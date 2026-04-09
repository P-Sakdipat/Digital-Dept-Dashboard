import pandas as pd
import numpy as np

file_path = 'd:/PoomAIWeb/DSI-Dashboard/zsdr003_datadic.xlsx'
df = pd.read_excel(file_path)

if not df.empty:
    base_row = df.iloc[0].copy()
    
    num_rows = 30000
    print(f"Generating {num_rows} mock rows...")
    
    start_vbeln = 4100100289
    
    customers = ['บริษัท ม็อค เอ จำกัด', 'Mock Company B', 'สำนักงานขาย ซี', 'Thai Trading Ltd.', 'Global Exports', 'Retail Corp']
    materials = ['3 PCS Laminate', 'Printed Cans', 'Unprinted Cans', 'Standard Base', 'Special Lid', 'Coated Steel']
    
    # Convert numpy output to proper types
    quantities = np.random.randint(1000, 100000, size=num_rows)
    returns_mask = np.random.random(num_rows) < 0.05
    quantities[returns_mask] = -np.abs(quantities[returns_mask] * np.random.uniform(0.1, 0.5, size=returns_mask.sum())).astype(int)
    
    prices = np.random.uniform(2.0, 5.0, size=num_rows)
    net_values = quantities * prices
    
    dates = np.random.randint(45659 - 365, 45659 + 30, size=num_rows)
    
    new_data = {col: [base_row[col]] * num_rows for col in df.columns}
    
    new_data['VBELN'] = np.arange(start_vbeln, start_vbeln + num_rows)
    new_data['FKDAT'] = dates
    new_data['Quantity'] = quantities
    new_data['NetValue'] = net_values
    new_data['LCValue'] = net_values
    new_data['TaxAmt'] = net_values * 0.07
    new_data['LCTax'] = net_values * 0.07
    new_data['SoldToName1'] = np.random.choice(customers, num_rows)
    new_data['MatGrDes'] = np.random.choice(materials, num_rows)
    
    df_mock = pd.DataFrame(new_data)
    
    print("Concatenating and saving to Excel... This might take a minute.")
    df_new = pd.concat([df, df_mock], ignore_index=True)
    df_new.to_excel(file_path, index=False)
    
    print(f"Successfully added {num_rows} mock rows to {file_path}")
else:
    print("DataFrame is empty.")
