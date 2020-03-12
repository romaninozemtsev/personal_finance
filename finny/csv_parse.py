from csv import DictReader, DictWriter
from datetime import datetime
import json
import os
from os.path import isfile, join
from os import listdir
import re
import pandas as pd
from definitions import config_path

from dateutil.parser import parse


columns_meta = {
    'Transaction Date#Post Date#Description#Category#Type#Amount': pd.read_csv(config_path('chase_columns.csv')),
    'Posted Date#Reference Number#Payee#Address#Amount': pd.read_csv(config_path('bofa_columns.csv')),
}


def read_transactions_file(tx_file_path):
    raw_df = pd.read_csv(tx_file_path)

    columns_meta_key = '#'.join(raw_df.columns)
    columns_df = columns_meta[columns_meta_key]

    rename_map = {}
    for index, row in columns_df.iterrows():
        rename_map[row['source_name']] = row['target_name']
    df = raw_df.rename(columns=rename_map)

    df['date'] = pd.to_datetime(df['date'])
    df['amount'] = df['amount'].astype(float)
    df['description'] = df['description'].str.lower().str.replace('\s+',' ', regex=True).str.strip()
    if 'address' not in df:
        df['address'] = '###'
    else:
        df['address'] = df['address'].str.lower().str.replace('\s+',' ', regex=True).str.strip().fillna('###')
    df.loc[df['amount'] > 0, 'type'] = 'credit' 
    df.loc[df['amount'] < 0, 'type'] = 'debit'
    return df


def read_transactions_from_folder(tx_file_folder):
    only_csv_files = [join(tx_file_folder, f) for f in listdir(tx_file_folder) if isfile(join(tx_file_folder, f)) and f.lower().endswith(".csv")]
    dfs = [read_transactions_file(x) for x in only_csv_files]
    df = pd.concat(dfs)
    return df

def write_enhanced_transactions(transactions_df, output_tx_file):
    transactions_df.to_csv(output_tx_file)
