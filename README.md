# Jupyter notebook (in python) to analyze spendings.

![notebook screenshot](docs/images/notebook_screenshot.png "Notebook screenshot")


### See example of notebook here
[notebook preview](https://github.com/romaninozemtsev/personal_finance/blob/master/parse_bank_statement.ipynb)


### Setup
```
git clone https://github.com/romaninozemtsev/personal_finance.git
python3 -m venv venv
source venv/bin/activate
```

### How to run interactive notebooks
```
(venv) jupyter notebook parse_bank_statement.ipynb
```

### Single command to convert csv folder to single enhanced CSV
```
(venv) python process_statements.py
```


### Open plot.ly dashboard with generated statement
```
(venv) python app.py
```


### Features wanted

1. group by merchant
2. group by category.
3. tag cloud
4. interactice transactions list
5. detect subscriptions
6. detect bills


### Tasks list

- [x] Bank Of America CSV parser
- [x] Chase CSV parser
- [ ] Better explicit schema for 'transaction' using typehints or smth like schmeatics.
- [x] Separate config file for Merchants
- [x] Description matchers should not apply tags. they come from merchant table.
- [ ] Web scraper instead of CSV
- [x] Parse entire folder of CSV filles (mix of BofA and Chase)
- [ ] default tags vs custom tags
- [ ] config list of known subscriptions (e.g netflix is always subscription, but apple can be one time or both)
- [ ] web app with interactive dashboard
- [ ] migrate current python dict code to pandas
- [ ] deduplicate transactions by either ref number or hash
- [ ] support checking/savings account transactions csv (BofA and Chase)


### How it works

1. raw transactions CSV data (different formats per bank)
2. cleaned and stadardized to common format
3. infer extra data from description - merchants, categories, subscriptions/bills 
4. display:
   1. notebook
   2. plot.ly app
