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
outer_join['Year 6 values'] = outer_join['Year 6'] * outer_join['num_seats']
outer_join['Year 7 values'] = outer_join['Year 7'] * outer_join['num_seats']
outer_join['Year 8 values'] = outer_join['Year 8'] * outer_join['num_seats']
outer_join['Year 9 values'] = outer_join['Year 9'] * outer_join['num_seats']
outer_join['Year 10 values'] = outer_join['Year 10'] * outer_join['num_seats']

# Change end_date to datetime
outer_join['end_date'] = pd.to_datetime(outer_join['end_date'])

# Create payment dates based on contract
outer_join['Year 1 dates'] = outer_join['end_date']
outer_join['Year 2 dates'] = outer_join['end_date'] + pd.offsets.DateOffset(years=1)
outer_join['Year 3 dates'] = outer_join['end_date'] + pd.offsets.DateOffset(years=2)
outer_join['Year 4 dates'] = outer_join['end_date'] + pd.offsets.DateOffset(years=3)
outer_join['Year 5 dates'] = outer_join['end_date'] + pd.offsets.DateOffset(years=4)
outer_join['Year 6 dates'] = outer_join['end_date'] + pd.offsets.DateOffset(years=5)
outer_join['Year 7 dates'] = outer_join['end_date'] + pd.offsets.DateOffset(years=6)
outer_join['Year 8 dates'] = outer_join['end_date'] + pd.offsets.DateOffset(years=7)
outer_join['Year 9 dates'] = outer_join['end_date'] + pd.offsets.DateOffset(years=8)
outer_join['Year 10 dates'] = outer_join['end_date'] + pd.offsets.DateOffset(years=9)

# Create new dataframes to enable concatenate to previous dataframe above deb
year1=outer_join[['acct_id', 'Year 1 values', 'Year 1 dates']]
year2=outer_join[['acct_id', 'Year 2 values', 'Year 2 dates']]
year3=outer_join[['acct_id', 'Year 3 values', 'Year 3 dates']]
year4=outer_join[['acct_id', 'Year 4 values', 'Year 4 dates']]
year5=outer_join[['acct_id', 'Year 5 values', 'Year 5 dates']]
year6=outer_join[['acct_id', 'Year 6 values', 'Year 6 dates']]
year7=outer_join[['acct_id', 'Year 7 values', 'Year 7 dates']]
year8=outer_join[['acct_id', 'Year 8 values', 'Year 8 dates']]
year9=outer_join[['acct_id', 'Year 9 values', 'Year 9 dates']]
year10=outer_join[['acct_id', 'Year 10 values', 'Year 10 dates']]

# Change column names for concate

year1.rename(columns={'Year 1 values': 'amount', 'Year 1 dates': 'payment date'}, inplace=True)
year2.rename(columns={'Year 2 values': 'amount', 'Year 2 dates': 'payment date'}, inplace=True)
year3.rename(columns={'Year 3 values': 'amount', 'Year 3 dates': 'payment date'}, inplace=True)
year4.rename(columns={'Year 4 values': 'amount', 'Year 4 dates': 'payment date'}, inplace=True)
year5.rename(columns={'Year 5 values': 'amount', 'Year 5 dates': 'payment date'}, inplace=True)
year6.rename(columns={'Year 6 values': 'amount', 'Year 6 dates': 'payment date'}, inplace=True)
year7.rename(columns={'Year 7 values': 'amount', 'Year 7 dates': 'payment date'}, inplace=True)
year8.rename(columns={'Year 8 values': 'amount', 'Year 8 dates': 'payment date'}, inplace=True)
year9.rename(columns={'Year 9 values': 'amount', 'Year 9 dates': 'payment date'}, inplace=True)
year10.rename(columns={'Year 10 values': 'amount', 'Year 10 dates': 'payment date'}, inplace=True)

# Concatenate the df's together
contracts = pd.concat([year1, year2, year3, year4, year5, year6, year7, year8, year9, year10, deb], ignore_index=True)

# Remove zero values
contracts= contracts[contracts['amount'] != 0]

# Change payment date to datetime
contracts['payment date'] = pd.to_datetime(contracts['payment date'])


# Read and slice Covid Credits csv
cov = pd.read_csv('Covid Credit.csv')
cov1 =cov[['acct_id','on_account_payments']]
cov1= cov1[cov1['on_account_payments'] != 0]

# Change 'acct_id' type to integer
contracts.fillna(0, inplace=True)
contracts['acct_id']= contracts['acct_id'].apply(np.int64)

# Add year & month column's to contracts
contracts['year'] = contracts['payment date'].dt.year
contracts['month'] = contracts['payment date'].dt.month

# Group by 'acct_id and 'year' and convert series to dataframe
acyr= contracts.groupby(['acct_id', 'year']).amount.sum()
acyrdf = acyr.unstack(level =1, fill_value=0)

# Clean data to show account id only from year 2021 to 2031
df = acyrdf.iloc[1:, 1:12]

# Merge cov1 with df
covdf= cov1.set_index('acct_id')
fulldf = pd.concat([df, covdf], axis=1)
fulldf = fulldf.fillna(0)









