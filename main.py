# Import panda

import pandas as pd

# Import Data
schdeb = pd.read_excel('Debtors.xlsx', sheet_name='Scheduled')
upfdeb = pd.read_excel('Debtors.xlsx', sheet_name='Upfront')
curdeb = pd.read_excel('Debtors.xlsx', sheet_name='Current')

# Clean Data to enable merge
schdeb.rename(columns={'CUSTNMBR': 'acct_id','PAYMENT AMOUNT' :'amount', 'DUEDATE': 'payment date'}, inplace=True)
schdeb3col = schdeb[['acct_id', 'amount', 'payment date']]
mask = (schdeb3col['payment date'] >= '01-10-2021')
schdeb3col = schdeb3col.loc[mask]

upfdeb['payment date'] = '2022-01-01'
upfdeb.rename(columns={'report_owed_amount':'amount'}, inplace='True')
upfdeb3col = upfdeb[['acct_id', 'amount', 'payment date']]

curdeb['payment date'] = '2022-01-01'
curdeb.rename(columns={'Customer Number':'acct_id', 'Customer Balance': 'amount'}, inplace=True)

# Concatenate the 3 data frames into one named deb
deb = pd.concat([schdeb3col, upfdeb3col, curdeb], ignore_index =True)

# Import data for future contract renewals and price plans
pp = pd.read_csv('Price Plans.csv')
con = pd.read_csv('Contracts.csv')

# Merge the two data frames
outer_join = pd.merge(con, pp, on='price_code',how='outer')
outer_join.fillna(0)

# Import Numpy
import numpy as np

# Convert objects to integer to allow numerical calculations
outer_join[["num_seats", "Year 1 ", "Year 2", "Year 3", "Year 4", "Year 5"]] = outer_join[["num_seats", "Year 1 ", "Year 2", "Year 3", "Year 4", "Year 5"]].apply(pd.to_numeric)
outer_join['Year 1 values'] = outer_join['Year 1 '] * outer_join['num_seats']
outer_join['Year 2 values'] = outer_join['Year 2'] * outer_join['num_seats']
outer_join['Year 3 values'] = outer_join['Year 3'] * outer_join['num_seats']
outer_join['Year 4 values'] = outer_join['Year 4'] * outer_join['num_seats']
outer_join['Year 5 values'] = outer_join['Year 5'] * outer_join['num_seats']

# Change end_date to datetime
outer_join['end_date'] = pd.to_datetime(outer_join['end_date'])

# Create payment dates based on contract
outer_join['Year 1 dates'] = outer_join['end_date']
outer_join['Year 2 dates'] = outer_join['end_date'] + pd.offsets.DateOffset(years=1)
outer_join['Year 3 dates'] = outer_join['end_date'] + pd.offsets.DateOffset(years=2)
outer_join['Year 4 dates'] = outer_join['end_date'] + pd.offsets.DateOffset(years=3)
outer_join['Year 5 dates'] = outer_join['end_date'] + pd.offsets.DateOffset(years=4)




