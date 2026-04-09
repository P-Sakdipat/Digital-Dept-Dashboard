import pandas as pd
df = pd.read_excel('zsdr003_datadic.xlsx')
neg_df = df[df['NetValue'] < 0]
print(f"Number of negative rows: {len(neg_df)}")
print(f"Sum of negative NetValue: {neg_df['NetValue'].sum()}")
print("Detailed negatives preview:")
print(neg_df[['VBELN', 'NetValue', 'Quantity']].head())
