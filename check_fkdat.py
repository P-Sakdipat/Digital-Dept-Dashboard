import pandas as pd
df = pd.read_excel('zsdr003_datadic.xlsx', nrows=5)
print(df['FKDAT'].head())
print("Data type:", df['FKDAT'].dtype)
