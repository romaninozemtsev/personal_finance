from finny import csv_parse
from finny import cleaner
from finny import enhance
    
if __name__ == "__main__":
    transactions = csv_parse.read_transactions_from_folder("personal/statements/")
    clean_txs = cleaner.clean_transactions(transactions)
    enhanced_txs = enhance.enhance_transactions(clean_txs)
    csv_parse.write_enhanced_transactions(enhanced_txs, "personal/my_transactions.csv")
