from dateutil.parser import parse
from typing import List
import re


def clean_description_from_address(tx):
    """See lots of transactions where Address is also appended to the description. Let's remove that."""
    address = tx["address"]
    description = tx['description']
    if description.startswith("sq *"):
        description = description.replace("sq *", "")
    elif description.startswith("tst* "):
        description = description.replace("tst* ", "")
    #print(address, description)
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
            #print("remove full address")
            return description.replace(address, '').strip()
        k = address.rfind(" ")
        address_without_last_space = address[:k]  + address[k+1:]
        #print(address_without_last_space)
        if description.endswith(address_without_last_space):
            #print("remove partial address")
            #print(description.replace(address_without_last_space, '').strip())
            return description.replace(address_without_last_space, '').strip()
    #print(description)
    return description


def clean_transactions(df):
    df['description'] = df.apply(clean_description_from_address, axis=1)
    return df
