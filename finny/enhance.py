import json
import re
import os

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

def enhance_transaction(tx):
    values_to_add = parse_description(tx["description"])
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
