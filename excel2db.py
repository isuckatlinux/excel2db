from sqlalchemy import *
import argparse
import pandas as pd
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help="path to excel file", type=str, required=True)
parser.add_argument('-u', '--user', help='Database username', type=str, required=True)
parser.add_argument('-p', '--password', help='Database password', type=str, required=True)
parser.add_argument('-n', '--name', help='Database name', type=str, required=True)
args = parser.parse_args()

def main():
    engine = create_engine(f"mysql+pymysql://{args.user}:{args.password}@localhost")
    dfs = []
    insp = inspect(engine)
    db_list = insp.get_schema_names()

    if args.name in db_list:
        print('Database already exist!')
        value = input('Do you want to overwrite it?[Y/N]')
        value = value.lower()
        if value == 'n':
            print('Exiting...')
            exit(0)

        engine.execute(f'drop database {args.name}')

    engine.execute(f'create database {args.name}')
    engine.execute(f'use {args.name}')
    file = args.file
    xls = pd.ExcelFile(file)
    sheets_names = xls.sheet_names
    for sheet_name in tqdm(sheets_names):
        df = pd.read_excel(xls, sheet_name)
        dfs.append(df)
        df.to_sql(sheet_name, engine, schema=args.name, index=False, if_exists='fail')

main()
