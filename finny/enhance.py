import re
import os
from definitions import config_path
import pandas as pd


matchers_category = pd.read_csv(config_path('matchers_category.csv'))
matchers_merchant = pd.read_csv(config_path('matchers_merchant.csv'))
merchants = pd.read_csv(config_path('merchants.csv')).set_index('merchant')
categories = pd.read_csv(config_path('categories.csv')).set_index('category')
categories['parent'] = categories['parent'].fillna('')


def find_merchant(description):
    for index, matcher in matchers_merchant.iterrows():
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
    return None, {}


def find_category(description):
    for index, matcher in matchers_category.iterrows():
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
    return merchants.loc[merchant]['category']


def find_root_category(category):
    parent = categories.loc[category]["parent"]
    if parent:
        return find_root_category(parent)
    else:
        return category


def parse_description(description):
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
    values_to_add = parse_description(tx["description"])
    if values_to_add:
        if "merchant" not in values_to_add:
            # TBD if this is what we want
            values_to_add["merchant"] = tx["description"]
        for k, v in values_to_add.items():
            tx[k] = v
    return tx


def enhance_transactions(transactions_df):
    return transactions_df.apply(enhance_transaction, axis=1)
