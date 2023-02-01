# (Donny)
#
# split a csv file into multiple files based on the value of a column. used for
# splitting up the csvs for the flow graphs. old openbudget used one file for
# every year, new one takes one file per chart
#
# usage: split_csv.py <csv_file> <column_name> <output_dir> [--txf "<lambda func for column_name transformation>"]
#  example of lambda 
# python3 split_csv.py test.csv Fiscal_Year _src/data/flow --txf "lambda x: 'FY' + str(x)[-2:]"
# This --txf transforms 2019 to FY19
# the default value for txf is the identity map
import os
import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file')
    parser.add_argument('column_name')
    parser.add_argument('output_dir')
    parser.add_argument('--txf', required=False, default='lambda x: x')
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    txf = eval(str(args.txf).replace('\\',''))
    df = pd.read_csv(args.csv_file)

    #calculate the list of unique column_name values
    buckets = df[args.column_name].unique()

    #loop through the unique column_name values
    for bkt in buckets:
        # write the file if it is not already there
        # NOTE: you must delete files in the target folder first if you want
        # to replace them... so that if there are multiple data sources for
        # the same year you won't accidentally overwrite the old ones
        filename = os.path.join(args.output_dir, '{}.csv'.format(txf(bkt)))
        if not os.path.exists(filename):
            df[df[args.column_name] == bkt].to_csv(filename, index=False)

if __name__ == '__main__':
    main()
