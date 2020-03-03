from dateutil.parser import parse
from typing import List
import re

        
def _clean_description_from_address(tx):
    """See lots of transactions where Address is also appended to the description. Let's remove that."""
    address = tx.get("address")
    description = tx['description']

    if not address:
        return description

    address_without_spaces = address.replace(' ', '')
    description_without_spaces = description.replace(' ', '')
    if description_without_spaces.endswith(address_without_spaces):
        # need to remove address from payee
        # possibilities are:
        # sunnyvale CA -> SunnyvaleCA
        # mountain view ca -> mountain viewca
        # sunnyvale ca -> sunnyvale ca
        if description.endswith(address):
            return description.replace(address, '').strip()
        k = address.rfind(" ")
        address_without_last_space = address[:k]  + address[k+1:]
        if description.endswith(address_without_last_space):
            return description.replace(address_without_last_space, '').strip()
    return description


def extract_point_of_sale(tx):
    pos_prefix = {
        "sq *": "square",
        "tst* ": "toast"
    }
    description = tx['description']
    for pos_tx_prefix, pos_name in pos_prefix.items():
        if description.startswith(pos_tx_prefix):
            tx['description'] = description.replace(pos_tx_prefix, '')
            tx['point_of_sale'] = pos_name


def _clean_transaction(transaction: dict):
    """Change field names to something that will be used with all the banks.
    
    also cleans up 'description' field from address.
    """
    formatted_tx = transaction.copy()
    extract_point_of_sale(formatted_tx)
    clean_description = _clean_description_from_address(formatted_tx)

    # square also prefixes their transactions with 'sq *', let's remove it.

    if formatted_tx['amount'] > 0:
        formatted_tx['type'] = 'credit'
    else:
        formatted_tx['type'] = 'debit'

    formatted_tx['description'] = clean_description
    return formatted_tx


def clean_transactions(transactions: List[dict]):
    """Cleans all transactions"""
    clean_txs = []
    for tx in transactions:
        clean_tx = _clean_transaction(tx)
        clean_txs.append(clean_tx)
    return clean_txs
