import pandas as pd
df = pd.read_excel('zsdr003_datadic.xlsx')
df['parsed_date'] = pd.to_datetime(df['dlDate'], format='%Y%m%d', errors='coerce')
target_date = pd.to_datetime('2026-04-06')
daily_df = df[df['parsed_date'] == target_date]
neg_df = daily_df[daily_df['NetValue'] < 0]

print("Negative Records on 2026-04-06:")
for idx, row in neg_df.iterrows():
    print(f"VBELN: {row['VBELN']}, POSNR: {row['POSNR']}, ARKTX: {row['ARKTX']}, NetValue: {row['NetValue']}, Quantity: {row['Quantity']}")
print(f"Total Returns: {neg_df['NetValue'].sum()}")
