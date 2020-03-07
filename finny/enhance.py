import json
import re
import os
from csv import DictReader

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(dir_path, '../configs/description_matchers.json')) as matchers_config:
    matchers = json.loads(matchers_config.read())

def try_match(description, matcher):
    match = matcher["match"]
    if match["type"] == "exact":
        if description == match["exact"]:
            return matcher["assign"]
    elif match["type"] == "keyword":
        parts = re.split(' |\.|,|\n', description)
        if match["keyword"] in parts:
            return matcher["assign"]
    elif match["type"] == "regex":
        re_match = re.match(match["regex"], description)
        if re_match:
            assign_values = matcher["assign"]
            if re_match.groupdict():
                assign_values.update(re_match.groupdict())
            return assign_values
    return None

def parse_description(description):
    for matcher in matchers:
        assign_values = try_match(description, matcher)
        if assign_values:
            return assign_values


def read_csv_config(config_name):
    with open(os.path.join(dir_path, '../configs/', config_name)) as config_file:
        reader = DictReader(config_file)
        return list(x for x in reader)

matchers_category = read_csv_config('matchers_category.csv')
matchers_merchant = read_csv_config('matchers_merchant.csv')
merchants = read_csv_config('merchants.csv')
categories = read_csv_config('categories.csv')

def find_merchant(description):
    for matcher in matchers_merchant:
        operation = matcher["operation"]
        expression = matcher["expression"]
        merchant = matcher["merchant"]
        if operation == "exact":
            if description == expression:
                return merchant, {}
        elif operation == "keyword":
            parts = re.split(' |\.|,|\n', description)
            if expression in parts:
                return merchant, {}
        elif operation == "regex":
            re_match = re.match(expression, description)
            if re_match:
                extra_values = {}
                if re_match.groupdict():
                    assign_values = re_match.groupdict()
                return merchant, extra_values
        return None

def find_category(description):
    for matcher in matchers_merchant:
        operation = matcher["operation"]
        expression = matcher["expression"]
        category = matcher["category"]
        if operation == "exact":
            if description == expression:
                return category
        elif operation == "keyword":
            parts = re.split(' |\.|,|\n', description)
            if expression in parts:
                return category
        elif operation == "regex":
            re_match = re.match(expression, description)
            if re_match:
                extra_values = {}
                if re_match.groupdict():
                    assign_values = re_match.groupdict()
                return category
        return None


def find_merchant_category(merchant):
    for m in merchants:
        if m["merchant"] == merchant:
            return m["category"]


def find_root_category(category):
    for c in categories:
        if c["category"] == category:
            if c["parent"]:
                return find_root_category(c["parent"])
            else:
                return category
    return category


def parse_tx2(description):
    merchant, extra_values = find_merchant(description)
    if merchant:
        category = find_merchant_category(merchant)
    else:
        category = find_category(description)
    if not category:
        category = "uncategorized"
    root_category = find_root_category(category)
    return dict(
        merchant=merchant,
        category=category,
        root_category=root_category,
        **extra_values
    )


def enhance_transaction(tx):
    values_to_add = parse_tx2(tx["description"])
    tx_copy = tx.copy()
    if values_to_add:
        if "merchant" not in values_to_add:
            # TBD if this is what we want
            values_to_add["merchant"] = tx["description"]
        tx_copy.update(values_to_add)
    
   
    return tx_copy

def enhance_transactions(transactions):
    result = []
    for tx in transactions:
        tx_copy = enhance_transaction(tx)
        result.append(tx_copy)
    return result
