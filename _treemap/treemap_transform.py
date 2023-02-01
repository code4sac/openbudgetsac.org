import sys, json, os
import pandas as pd
import numpy as np

def load_config(cfg_file):
    '''
    Directly loads a config .json file. This .json file specifies the way that 
    each treemap .json file is built, including how to pivot the data.

    cfg_file --> the path to the config .json file to load 
    '''
    if os.path.exists(cfg_file): # check for the file
        try:
            return json.load(open(cfg_file)) # load and parse json text to object
        except Exception as ex:
            print ("Couldn't parse .json file: {}\n\t{}".format(cfg_file, ex))
            return json.loads("{}") # empty object
    else:
        print ("File", cfg_file, "is missing.")
        return json.loads("{}") # empty object

def load_csv_data(csv_file):
    '''
    Directly loads a budget .csv file. This .csv file contains all relevant
    budget data in a tabular format. The config.json file refers to column names
    that are in the .csv file in its instructions. This function loads .csv data
    into a pandas DataFrame.

    csv_file --> the path to the budget .csv file to load 
    '''
    if os.path.exists(csv_file): # check for the file
        try:
            return pd.read_csv(csv_file) # load it into a pandas dataframe
        except Exception as ex:
            print ("Couldn't parse .csv file: {}\n\t{}".format(csv_file, ex))
            return pd.DataFrame() # blank dataframe
    else:
        print ("File", csv_file, "is missing")
        return pd.DataFrame() # blank dataframe

def filter_df(df, **filter):
    '''
    Filters a pandas data frame with equality slicers determined by the filters. This method
    is recursive and applies one filter key-value pair at a time sequentially.

    df --> the DataFrame to filter
    **filter --> a list of param names and filter values e.g.,
        filter_df(df, Fund='Zoo Fund')
        This filter in the example above returns a smaller data frame in which the Fund is always 'Zoon Fund'
    '''
    if len(filter) == 0: return df # no filtering left to do
    
    key, val = filter.popitem() # remove the next filter
    try:
        val=int(val) # if numeric, we will integerize, otherwise string is assumed
    except:
        pass

    # call down to next filter level after filtering this level
    # note that the data frame below is filtered by the current filter and the filter
    # below no longer includes the current filter, so this recursion is convergent
    return filter_df(df[df[key]==val], **filter)

def compute_parent_child_index(idx):
    '''
    This method splits a dataframe index into the parent parts and the child part.
    The assumption is that the index is multi-column and that the last entry denotes the child.
    The prior entries denote layers of tree-parentage e.g., genenerations in the tree that are
        above this particular child.
    If the index is not a tuple, or it is a 1-tuple, this is an unparented node in the tree
        i.e., there are multiple trees.

    idx --> the index key to split up (if relevant) into parent and child
    '''
    if type(idx) == tuple: # pivoted data frame indices are tuples if multiple columns are in index
        if len(idx) > 1: # either we need to split out the last index as the child
            return list(idx[0:-1]), idx[-1]
        else: # or we need to note an empty parent and return the only item as the child
            return [], idx[0]
    else: # if the index isn't a tuple it should be passed through with no parent
        return [], idx

def place_value_in_tree(tree, parent, child, **data):
    '''
    First we will recursively construct a dictionary tree structure representing the hierarchy
    of the data columns per the config .json file. This recursion works by leveraging the
    ability of the dictionary to be navigated by key. This result is not especially performant, 
    but the current data size is small so further optimization is probably not required.

    tree --> the dictionary subtree node to traverse
    parent --> a list of keys above this data in the hierarchy
    child --> the key below the parent to which this treemap data belongs
    **data --> the attributes that are data for this treenode in the hierarchy
    '''
    if parent is None or len(parent) == 0: 
        # if there is no parent, we will record this item in the root note of the current subtree
        tree[child] = dict(data=data, key=child)
    else:
        # we will remove the top level parent key and recurse through it into the correct subtree
        key = parent.pop(0)
        place_value_in_tree(tree[key], parent, child, **data) #recurse, note the subtree and 
                                        # recall that the parent index is relative to the subtree

def transform_branch_to_branch(tree):
    '''
    Next we will take the dictionary tree structure produced in place_value_in_tree and reform
    it into the structure that the treemap prefers. This part of the approach is also not ideal,
    but with small data sizes is adequately performant.

    Once again, this method is recursive and it recurses through the tree resulting from the
    place_value_in_tree function only through keys that are not 'data' and not 'key' as these are
    not recursing attributes but rather treenode attributes.

    tree --> the subtree to transform from the dictionary tree structure to the .json treemap
             structure required by D3.js 
    '''
    ret_tree = dict() # create a dictionary node for this subtree (could be the whole tree)

    # first we will transform all the child nodes of the root of this subtree (recursive)
    if len(set(tree.keys()).difference(set(['key','data']))) > 0: 
        # in particular instead of a separate key for each tree node with its own name
        # we will be grouping them into a values list, but each of those values may have
        # a further subtree to traverse and transform.
        ret_tree['values'] = [
            transform_branch_to_branch(v) # hence this recursion step
            for k, v in tree.items() 
            if k not in ['data', 'key'] # only recurse on keys that are not data or key
        ]
    
    # the data and key for this node are simply recorded as attributes of the subtree root node
    if 'data' in tree: ret_tree['data'] = tree['data']
    if 'key' in tree: ret_tree['key'] = tree['key']

    # we are done with this branch
    return ret_tree


def transform_group_to_files(df, group, grouping_headers, amount_header):
    '''
    A group from the config .json is used to guide the process of 
    1. Filtration of the DataFrame from the .csv file
    2. Construction of an easily traversable dictionary tree
    3. Transformation of the dictionary tree into the D3.js treemap format
    '''
    # compte the filters argument for reducing the dataframe
    filters = {key: val for key, val in zip(grouping_headers, group["values"])}

    # reduce the dataframe (store data in .csv for diagnostic purposes TODO comment out)
    reduced_df = filter_df(df, **filters)
    # reduced_df.to_csv(group['filename']+'.csv', index=False)

    # begin with a blank dictionary
    tree_dict = dict()

    # construct the tree leveraging dictionary starting at the top
    #   we'll iterate through the levels of the hierarchy to construct the hierarchy
    #   each level will be keyed to the portion of the hierarchy index appropriate to that level
    #   to get correct totals for aggregated layers, we will pivot to that portion of the hierarchy
    for i in range(len(group['hierarchy'])):

        # pandas pivot_tables let us accurately, progressively, and simply identify the hierarchy
        # and iterate it in order to construct the various levels of the dictionary tree 
        pvt = pd.pivot_table(reduced_df, values=amount_header, index=group['hierarchy'][:i+1], aggfunc=np.sum)
        #print(pvt.index)

        # at the ith level of the hierarchy we can now construct this layer of the dictionary tree
        for idx in pvt.index:
            # the parent index lets us know how to traverse to this level and the child index tells us how to tag the new level
            pidx, cidx = compute_parent_child_index(idx)

            # place the data in the tree, all nodes have three values: amount, expense, and revenue
            place_value_in_tree(
                tree_dict, pidx, cidx, 
                amount=float(pvt[amount_header][idx]), 
                expense=float(pvt[amount_header][idx] * (1.0 if group['values'][0] == 'E' else 0)), 
                revenue=float(pvt[amount_header][idx] * (1.0 if group['values'][0] == 'R' else 0))
            )

    # write the data transformed into D3.js treemap format into the filename specified in the group
    json.dump(transform_branch_to_branch(tree_dict), open(group['filename'],'w'))


def pull_groups(df, cfg):
    '''
    Transform the raw data using the config file

    df --> the DataFrame from loading the .csv file
    cfg --> the json object from loading config .json file
    '''
    if 'groups' not in cfg:
        print('config .json file is not correctly formatted')
        return
    if len(df.columns) * len(df.index) == 0: 
        print('The .csv file is either incorrectly formatted or empty')
        return
    for group in cfg["groups"]:
        transform_group_to_files(df, group, cfg["grouping_headers"], cfg["amount_header"])

def main():
    '''
    Load the configuration, load the raw data from .csv, then transform it all
    '''
    print(*sys.argv)
    if len(sys.argv) != 3:
        print ("This script requires two extra arguments: <config>.json <budget data>.csv")
    
    cfg = load_config(sys.argv[1]) # load the config file

    df = load_csv_data(sys.argv[2]) # load the csv data

    pull_groups(df, cfg)

if __name__ == '__main__':
    main()