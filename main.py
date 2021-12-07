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

# Create values for each year based on number of seats
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

# Add year column to contracts
contracts['year'] = contracts['payment date'].dt.year

# Group by 'acct_id and 'year' and convert series to dataframe
acyr= contracts.groupby(['acct_id', 'year']).amount.sum()
acyrdf = acyr.unstack(level =1, fill_value=0)

# Clean data to show account id only from year 2021 to 2031
df = acyrdf.iloc[1:, 1:12]

# Merge cov1 with df
covdf= cov1.set_index('acct_id')
fulldf = pd.concat([df, covdf], axis=1)
fulldf = fulldf.fillna(0)

#Create new columns for each year
conditions = (fulldf[2021]<= fulldf['on_account_payments']) , (fulldf[2021]>fulldf['on_account_payments'])
choices = [fulldf[2021], fulldf['on_account_payments']]
fulldf['Covid 2021'] = np.select(conditions, choices)
fulldf['credit bal 22'] = fulldf['on_account_payments'] - fulldf['Covid 2021']
fulldf['Payment 2021'] = fulldf[2021] - fulldf['Covid 2021']


conditions2 = (fulldf[2022]<= fulldf['credit bal 22']) , (fulldf[2021]>fulldf['credit bal 22'])
choices2 = [fulldf[2022], fulldf['credit bal 22']]
fulldf['Covid 2022'] = np.select(conditions2, choices2)
fulldf['credit bal 23'] = fulldf['credit bal 22'] - fulldf['Covid 2022']
fulldf['Payment 2022'] = fulldf[2022] - fulldf['Covid 2022']

conditions3 = (fulldf[2023]<= fulldf['credit bal 23']) , (fulldf[2023]>fulldf['credit bal 23'])
choices3 = [fulldf[2023], fulldf['credit bal 23']]
fulldf['Covid 2023'] = np.select(conditions3, choices3)
fulldf['credit bal 24'] = fulldf['credit bal 23'] - fulldf['Covid 2023']
fulldf['Payment 2023'] = fulldf[2023] - fulldf['Covid 2023']

conditions4 = (fulldf[2024]<= fulldf['credit bal 24']) , (fulldf[2024]>fulldf['credit bal 24'])
choices4 = [fulldf[2024], fulldf['credit bal 24']]
fulldf['Covid 2024'] = np.select(conditions4, choices4)
fulldf['credit bal 25'] = fulldf['credit bal 24'] - fulldf['Covid 2024']
fulldf['Payment 2024'] = fulldf[2024] - fulldf['Covid 2024']

conditions5 = (fulldf[2025]<= fulldf['credit bal 25']) , (fulldf[2025]>fulldf['credit bal 25'])
choices5 = [fulldf[2025], fulldf['credit bal 25']]
fulldf['Covid 2025'] = np.select(conditions5, choices5)
fulldf['credit bal 26'] = fulldf['credit bal 25'] - fulldf['Covid 2025']
fulldf['Payment 2025'] = fulldf[2025] - fulldf['Covid 2025']

conditions6 = (fulldf[2026]<= fulldf['credit bal 26']) , (fulldf[2026]>fulldf['credit bal 26'])
choices6 = [fulldf[2026], fulldf['credit bal 26']]
fulldf['Covid 2026'] = np.select(conditions6, choices6)
fulldf['credit bal 27'] = fulldf['credit bal 26'] - fulldf['Covid 2026']
fulldf['Payment 2026'] = fulldf[2026] - fulldf['Covid 2026']

conditions7 = (fulldf[2027]<= fulldf['credit bal 27']) , (fulldf[2027]>fulldf['credit bal 27'])
choices7 = [fulldf[2027], fulldf['credit bal 27']]
fulldf['Covid 2027'] = np.select(conditions7, choices7)
fulldf['credit bal 28'] = fulldf['credit bal 27'] - fulldf['Covid 2027']
fulldf['Payment 2027'] = fulldf[2027] - fulldf['Covid 2027']

conditions8 = (fulldf[2028]<= fulldf['credit bal 28']) , (fulldf[2028]>fulldf['credit bal 28'])
choices8 = [fulldf[2028], fulldf['credit bal 28']]
fulldf['Covid 2028'] = np.select(conditions8, choices8)
fulldf['credit bal 29'] = fulldf['credit bal 28'] - fulldf['Covid 2028']
fulldf['Payment 2028'] = fulldf[2028] - fulldf['Covid 2028']

conditions9 = (fulldf[2029]<= fulldf['credit bal 29']) , (fulldf[2029]>fulldf['credit bal 29'])
choices9 = [fulldf[2029], fulldf['credit bal 29']]
fulldf['Covid 2029'] = np.select(conditions9, choices9)
fulldf['credit bal 30'] = fulldf['credit bal 29'] - fulldf['Covid 2029']
fulldf['Payment 2029'] = fulldf[2029] - fulldf['Covid 2029']

conditions10 = (fulldf[2030]<= fulldf['credit bal 30']) , (fulldf[2030]>fulldf['credit bal 30'])
choices10 = [fulldf[2030], fulldf['credit bal 30']]
fulldf['Covid 2030'] = np.select(conditions10, choices10)
fulldf['credit bal 31'] = fulldf['credit bal 30'] - fulldf['Covid 2030']
fulldf['Payment 2030'] = fulldf[2030] - fulldf['Covid 2030']

conditions11 = (fulldf[2031]<= fulldf['credit bal 31']) , (fulldf[2031]>fulldf['credit bal 31'])
choices11 = [fulldf[2031], fulldf['credit bal 31']]
fulldf['Covid 2031'] = np.select(conditions11, choices11)
fulldf['credit bal 32'] = fulldf['credit bal 31'] - fulldf['Covid 2031']
fulldf['Payment 2031'] = fulldf[2031] - fulldf['Covid 2031']

# Get Total of all columns
dfsum =fulldf.sum(axis = 0, skipna =True)
dfmm = dfsum.to_frame().reset_index()

# Add years & category for plotting.
dfmm['Years'] =[2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2021, 2021, 2022, 2021, 2022, 2023, 2022, 2023, 2024, 2023, 2024, 2025, 2024, 2025, 2026, 2025, 2026, 2027, 2026, 2027, 2028, 2027, 2028, 2029, 2028, 2029, 2030, 2029, 2030, 2031, 2030, 2031, 2032, 2031]
dfmm['category'] = ['year', 'year', 'year', 'year', 'year', 'year', 'year', 'year', 'year', 'year', 'year', 'covid', 'covid', 'covid', 'payment','covid', 'covid', 'payment','covid', 'covid','payment','covid', 'covid','payment','covid', 'covid', 'payment','covid', 'covid', 'payment','covid', 'covid', 'payment','covid','covid', 'payment','covid','covid', 'payment','covid','covid', 'payment','covid', 'covid', 'payment']
dfforplot = dfmm.iloc[[12, 14, 15, 17, 18, 20, 21, 23, 24, 26, 27, 29, 30, 32, 33, 35, 36, 38, 39, 41, 42 , 44 ]]

# Import matplotlib and seaborn
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches

# Plot dataframe as a stacked bar chart
sns.set(style='darkgrid')
plt.figure(figsize=(14,14))
total = dfforplot.groupby('Years')[0].sum().reset_index()
bar1 = sns.barplot(x='Years', y=0, data=total, color='darkblue').set(title= 'Cashflow Forecast Premium Seats 2021 to 2031', ylabel='10s of Millions')
payment = dfforplot[dfforplot.category=='payment']
bar2 = sns.barplot(x ='Years', y=0, data=payment, estimator=sum, ci=None, color='lightblue').set(title= 'Cashflow Forecast Premium Seats 2021 to 2031', ylabel='10s of Millions')
top_bar = mpatches.Patch(color='darkblue', label='Covid credit used')
bottom_bar = mpatches.Patch(color='lightblue', label='Payment')
plt.legend(handles=[top_bar, bottom_bar])
plt.show()
plt.close()



