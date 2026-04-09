import pandas as pd
df = pd.read_excel('zsdr003_datadic.xlsx')
# Filter for 20260406
df['parsed_date'] = pd.to_datetime(df['dlDate'], format='%Y%m%d', errors='coerce')
target_date = pd.to_datetime('2026-04-06')
daily_df = df[df['parsed_date'] == target_date]

gross = daily_df[daily_df['NetValue'] > 0]['NetValue'].sum()
returns = daily_df[daily_df['NetValue'] < 0]['NetValue'].sum()
net = daily_df['NetValue'].sum()
lc_sum = daily_df['LCValue'].sum()

print("==== DATE: 2026-04-06 ====")
print(f"Gross Sales: {gross:,.2f}")
print(f"Returns:     {returns:,.2f}")
print(f"Net Revenue: {net:,.2f}")
print(f"LC Value:    {lc_sum:,.2f}")

