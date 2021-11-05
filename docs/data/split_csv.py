# (Donny)
#
# split a csv file into multiple files based on the value of a column. used for
# splitting up the csvs for the flow graphs. old openbudget used one file for
# every year, new one takes one file per chart
#
# usage: split_csv.py <csv_file> <column_name> <output_dir>
def main():
    import sys
    import os
    import csv
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file')
    parser.add_argument('column_name')
    parser.add_argument('output_dir')
    args = parser.parse_args()
    csv_file = args.csv_file

    column_name = args.column_name
    output_dir = args.output_dir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            value = row[column_name]
            filename = os.path.join(output_dir, value + '.csv')
            with open(filename, 'a') as f:
                writer = csv.DictWriter(f, reader.fieldnames)
                writer.writerow(row)


main()
