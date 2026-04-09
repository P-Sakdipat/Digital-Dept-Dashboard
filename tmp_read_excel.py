import pandas as pd
import json

try:
    df = pd.read_excel('zsdr003_datadic.xlsx')
    info = {
        'columns': list(df.columns),
        'row_count': len(df),
        'sample': df.head(3).to_dict(orient='records')
    }
    with open('tmp_info.json', 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    print("SUCCESS: info dumped to tmp_info.json")
except Exception as e:
    print(f"ERROR: {e}")
