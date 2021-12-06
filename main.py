# Import packages

import numpy as np
import pandas as pd

# Import Data
schdeb = pd.read_excel('Debtors.xlsx', sheet_name='Scheduled')
upfdeb = pd.read_excel('Debtors.xlsx', sheet_name='Upfront')
curdeb = pd.read_excel('Debtors.xlsx', sheet_name='Current')

# Clean Data to enable merge
schdeb.rename(columns={'CUSTNMBR': 'acct_id','PAYMENT AMOUNT':'amount', 'DUEDATE': 'payment date' }, inplace =True)
schdeb3col = schdeb[['acct_id', 'amount', 'payment date']]
mask = (schdeb3col['payment date'] >= '01-10-2021')
schdeb3col = schdeb3col.loc[mask]

upfdeb['payment date'] = '2022-01-01'
upfdeb.rename(columns={'report_owed_amount':'amount'}, inplace='True')
upfdeb3col = upfdeb[['acct_id', 'amount', 'payment date']]

curdeb['payment date'] = '2022-01-01'
curdeb.rename(columns={'Customer Number':'acct_id', 'Customer Balance': 'amount'}, inplace=True)


