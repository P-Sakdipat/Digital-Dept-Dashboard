import pandas as pd
df = pd.read_excel('zsdr003_datadic.xlsx')
record = df[df['VBELN'] == 4130002327]
if not record.empty:
    print(record[['dlDate', 'FKDAT', 'VBELN', 'NetValue', 'Quantity']])
else:
    print("Record not found!")
