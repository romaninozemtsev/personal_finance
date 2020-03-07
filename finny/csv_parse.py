from csv import DictReader, DictWriter
from datetime import datetime
import json
import os
from os.path import isfile, join
from os import listdir
import re

from dateutil.parser import parse

dir_path = os.path.dirname(os.path.realpath(__file__))

def _read_column_file(columns_meta_file_name):
    with open(columns_meta_file_name) as columns_meta_file:
        return json.loads(columns_meta_file.read())

columns_meta = {
    'Transaction Date#Post Date#Description#Category#Type#Amount': _read_column_file(join(dir_path, '../configs/chase_columns.json')),
    'Posted Date#Reference Number#Payee#Address#Amount': _read_column_file(join(dir_path,'../configs/bofa_columns.json'))
}

def _clean_name_and_type(key: str, value: str, columns_meta: dict):
    """Takes key, value and returns new key, value
    
    For example:
    standardize_item("Amount", "27.97") returns ("amount", 27.97)
    """
    column_meta = columns_meta[key]
    new_key = column_meta["name"]
    column_type = column_meta["type"]
    if column_type == "datetime":
        new_value = parse(value)
    elif column_type == "float":
        new_value = float(value)
    elif column_type == "str":
        new_value = str(value)
        new_value = re.sub('\s+',' ', new_value.lower().strip())
    else:
        raise Exception("unknown column type")
    return new_key, new_value


def _clean_transaction(tx: dict, columns_meta: dict):
    formatted_tx = {}
    for k, v in tx.items():
        new_key, new_value = _clean_name_and_type(k, v, columns_meta)
        formatted_tx[new_key] = new_value
    return formatted_tx


def read_transactions_file(tx_file_path):
    with open(tx_file_path) as csvfile:
        reader = DictReader(csvfile)
        columns_meta_key = '#'.join(reader.fieldnames)
        columns_defs = columns_meta.get(columns_meta_key)
        if not columns_defs:
            raise Exception("unknown CSV format " + ','.join(reader.fieldnames))
        transactions_list = list(_clean_transaction(dict(x), columns_defs) for x in reader)
        return transactions_list

def read_transactions_from_folder(tx_file_folder):
    only_csv_files = [join(tx_file_folder, f) for f in listdir(tx_file_folder) if isfile(join(tx_file_folder, f)) and f.lower().endswith(".csv")]
    all_transactions = []
    for csv_file in only_csv_files:
        all_transactions.extend(read_transactions_file(csv_file))
    return all_transactions

def write_enhanced_transactions(transactions, output_tx_file):
    with open(output_tx_file, 'w') as csvfile:
        fieldnames = [
            "date","ref_num","description","address","amount",
            "type","merchant","category","root_category","tags","merchant_location","order_number",
            "point_of_sale", "bank_tx_type", "bank_category", "tx_date"
        ]
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transactions)
