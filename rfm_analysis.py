from datetime import datetime
import pandas as pd

data_type = ({
    "CustomerID": str
})


sales_data = pd.read_csv(
    "sales_data.csv", dtype=data_type, parse_dates=['OrderDate'])

df = sales_data.copy()
df['Revenue'] = (df['Unit Price'] - (df['Unit Price'] *
                 df['Discount Applied']) - df['Unit Cost'])*df['Order Quantity']

columns = ['OrderNumber', '_CustomerID', 'OrderDate', 'Revenue']
df_dataset = df[columns]
today_date = pd.to_datetime('2021-01-01')
rfm_dataset = df_dataset.groupby('_CustomerID').agg({'OrderDate': lambda v: (
    today_date - v.max()).days, 'OrderNumber': 'count', 'Revenue': 'sum'})


rfm_dataset.rename(columns={'OrderDate': 'recency',
                   'OrderNumber': 'frequency', 'Revenue': 'monetory'}, inplace=True)

r = pd.qcut(rfm_dataset['recency'], q=5, labels=range(5, 0, -1))
f = pd.qcut(rfm_dataset['frequency'], q=5, labels=range(1, 6))
m = pd.qcut(rfm_dataset['monetory'], q=5, labels=range(1, 6))


rfm = rfm_dataset.assign(R=r.values, F=f.values, M=m.values)

rfm['rfm_group'] = rfm[['R', 'F', 'M']].apply(
    lambda v: '-'.join(v.astype(str)), axis=1)
rfm['rfm_score_total'] = rfm[['R', 'F', 'M']].sum(axis=1)
print(rfm)
