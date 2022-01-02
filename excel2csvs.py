import argparse
import pandas as pd
import os
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help="path to file", type=str, required=True)
parser.add_argument('-d', '--directory', help="path to the folder where csvs are going to be stored", type=str)
args = parser.parse_args()


def check_file_exist(file):
    try:
        with open(file) as f:
            return True
    except IOError:
        raise Exception("File not accessible!")


def check_directory(dir):
    if not os.path.isdir(dir):
        raise Exception(f'Directory {dir} not found!')


def main():
    file = args.file
    check_file_exist(file)

    directory_to_save = '.'
    if args.directory is not None:
        directory_to_save = args.directory
    check_directory(directory_to_save)
    xls = pd.ExcelFile(file)
    sheets_names = xls.sheet_names
    for sheet_name in tqdm(sheets_names):
        df = pd.read_excel(xls, sheet_name)
        df.to_csv(f'{directory_to_save}/{sheet_name}.csv', index=False)


main()
