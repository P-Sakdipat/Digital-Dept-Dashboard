import os
import pandas as pd
import numpy as np
import requests
from threading import Lock

SHEETY_URL = 'https://api.sheety.co/0ba89f822371268e238784616b6edce5/dsiDatadic/ชีต1'

# Mapping from Sheety's camelCase keys back to original Python code's Exact casing
COLUMN_MAPPING_TO_ORIGINAL = {
    'dlDate': 'dlDate', 'fkdat': 'FKDAT', 'vbeln': 'VBELN', 'posnr': 'POSNR', 'matnr': 'MATNR', 
    'arktx': 'ARKTX', 'billReturn': 'BillReturn', 'quantity': 'Quantity', 'netValue': 'NetValue', 
    'taxAmt': 'TaxAmt', 'lcValue': 'LCValue', 'lcTax': 'LCTax', 'priceDate': 'PriceDate', 
    'exRate': 'ExRate', 'crPrice': 'CrPrice', 'currency': 'Currency', 'refDoc': 'RefDoc', 
    'refItem': 'RefItem', 'salesDoc': 'SalesDoc', 'salesItem': 'SalesItem', 'matGr': 'MatGr', 
    'matGrDes': 'MatGrDes', 'itemCat': 'ItemCat', 'billType': 'BillType', 'billCat': 'BillCat', 
    'docCat': 'DocCat', 'salesOrg': 'SalesOrg', 'disChannel': 'DisChannel', 'custGr': 'CustGr', 
    'nWeight': 'NWeight', 'gWeight': 'GWeight', 'weightUnit': 'WeightUnit', 'district': 'district', 
    'destCty': 'DestCty', 'vrkme': 'VRKME', 'mvgr1': 'MVGR1', 'mvgr2': 'MVGR2', 'mvgr3': 'MVGR3', 
    'mvgr4': 'MVGR4', 'mvgr5': 'MVGR5', 'soldTo': 'SoldTo', 'soldToName1': 'SoldToName1', 
    'soldToName2': 'SoldToName2', 'soldToName3': 'SoldToName3', 'reason': 'Reason', 
    'reasonDes': 'ReasonDes', 'referS': 'ReferS', 'pono': 'PONO', 'poDate': 'PODate', 
    'salesPrice': 'SalesPrice', 'priceUnit': 'PriceUnit', 'mvgr1D': 'MVGR1D', 'mvgr3D': 'MVGR3D', 
    'mvgr4D': 'MVGR4D', 'term': 'Term', 'termDes': 'TermDes', 'cancel': 'Cancel', 
    'cancelBill': 'CancelBill', 'empNo': 'EmpNO', 'empName': 'EmpName', 'shipTo': 'ShipTo', 
    'shipToName1': 'ShipToName1', 'shipToName2': 'ShipToName2', 'shipToName3': 'ShipToName3', 
    'id': 'id'
}

# Reverse mapping for sending data back to Sheety
COLUMN_MAPPING_TO_SHEETY = {v: k for k, v in COLUMN_MAPPING_TO_ORIGINAL.items() if k != 'id'}

class ExcelDB:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(ExcelDB, cls).__new__(cls)
                    cls._instance.df = None
                    cls._instance.load_data()
        return cls._instance

    def load_data(self):
        try:
            print("Fetching data from Sheety...")
            response = requests.get(SHEETY_URL)
            if response.status_code == 200:
                data = response.json().get('ชีต1', [])
                self.df = pd.DataFrame(data)
                self.df = self.df.rename(columns=COLUMN_MAPPING_TO_ORIGINAL)
                
                # Replace empty strings or NaNs with None for JSON serialization
                self.df = self.df.replace({np.nan: None, "": None})
                print(f"Successfully loaded {len(self.df)} rows from Sheety.")
            else:
                print(f"Error loading Sheety data. Status code: {response.status_code}")
                self.df = pd.DataFrame()
        except Exception as e:
            print(f"Error making request to Sheety: {e}")
            self.df = pd.DataFrame()

    def save_data(self):
        # We no longer save to a local Excel file.
        # Data is synced directly to Sheety on individual modifications.
        pass

    def get_all(self):
        return self.df.to_dict(orient='records')
        
    def get_paginated(self, page=1, page_size=100, filters=None):
        df_filtered = self.df.copy()
        
        if filters:
            for key, value in filters.items():
                if value and key in df_filtered.columns:
                    # Simple string contains filter for most text fields
                    # Exact match for others, convert type safely
                    if df_filtered[key].dtype == object:
                        df_filtered = df_filtered[df_filtered[key].astype(str).str.contains(value, case=False, na=False)]
                    else:
                        try:
                            df_filtered = df_filtered[df_filtered[key] == type(df_filtered[key].iloc[0])(value)]
                        except:
                            pass

        total = len(df_filtered)
        start = (page - 1) * page_size
        end = start + page_size
        paginated_data = df_filtered.iloc[start:end].to_dict(orient='records')
        
        return {
            'data': paginated_data,
            'total': total,
            'page': page,
            'page_size': page_size
        }

    def add_row(self, row_data):
        # Map original keys back to Sheety keys
        sheety_data = {}
        for key, value in row_data.items():
            if key in COLUMN_MAPPING_TO_SHEETY and value is not None:
                sheety_data[COLUMN_MAPPING_TO_SHEETY[key]] = value
                
        payload = {"ชีต1": sheety_data}
        try:
            response = requests.post(SHEETY_URL, json=payload)
            if response.status_code in [200, 201]:
                # Sheety returns the created object with the assigned 'id'
                result = response.json().get('ชีต1', {})
                if result:
                    mapped_result = {COLUMN_MAPPING_TO_ORIGINAL.get(k, k): v for k, v in result.items()}
                    new_row = pd.DataFrame([mapped_result])
                    self.df = pd.concat([self.df, new_row], ignore_index=True)
                else:
                    self.load_data()  # Fallback
                return True
            else:
                print(f"Error adding to Sheety: {response.text}")
        except Exception as e:
            print(f"Error adding row to Sheety: {e}")
            
        return False

    def update_row(self, vbeln, posnr, row_data):
        mask = (self.df['VBELN'] == vbeln) & (self.df['POSNR'] == posnr)
        if not mask.any():
            return False
            
        row_id = self.df.loc[mask, 'id'].values[0]
        if pd.isna(row_id):
            print("Cannot update: row ID is missing")
            return False
            
        update_url = f"{SHEETY_URL}/{int(row_id)}"
        
        # Build payload
        sheety_data = {}
        for key, value in row_data.items():
            if key in COLUMN_MAPPING_TO_SHEETY and value is not None:
                sheety_data[COLUMN_MAPPING_TO_SHEETY[key]] = value
                
        payload = {"ชีต1": sheety_data}
        try:
            response = requests.put(update_url, json=payload)
            if response.status_code in [200, 201]:
                # Update local dataframe
                for key, value in row_data.items():
                    if key in self.df.columns:
                        self.df.loc[mask, key] = value
                return True
            else:
                print(f"Error updating Sheety: {response.text}")
        except Exception as e:
            print(f"Error updating row in Sheety: {e}")
            
        return False

    def delete_row(self, vbeln, posnr):
        mask = (self.df['VBELN'] == vbeln) & (self.df['POSNR'] == posnr)
        if not mask.any():
            return False
            
        row_id = self.df.loc[mask, 'id'].values[0]
        if pd.isna(row_id):
            print("Cannot delete: row ID is missing")
            return False
            
        delete_url = f"{SHEETY_URL}/{int(row_id)}"
        
        try:
            response = requests.delete(delete_url)
            if response.status_code in [200, 204]:
                self.df = self.df[~mask]
                return True
            else:
               print(f"Error deleting from Sheety: {response.text}") 
        except Exception as e:
            print(f"Error deleting row in Sheety: {e}")
            
        return False

    def get_summary(self, time_filter='all', ref_date=None):
        df_summary = self.df.copy()
        if 'FKDAT' in df_summary.columns and time_filter != 'all':
            # Sheety sometimes returns numbers as strings if they are formatted strangely, parse date carefully
            df_summary['parsed_date'] = pd.to_datetime(pd.to_numeric(df_summary['FKDAT'], errors='coerce'), unit='D', origin='1899-12-30', errors='coerce')
            
            target_date = None
            if ref_date:
                try:
                    target_date = pd.to_datetime(ref_date)
                except:
                    target_date = df_summary['parsed_date'].max()
            else:
                target_date = df_summary['parsed_date'].max()
                
            if pd.notnull(target_date):
                if time_filter == 'day':
                    df_summary = df_summary[df_summary['parsed_date'] == target_date]
                elif time_filter == 'week':
                    import datetime
                    start_date = target_date - pd.Timedelta(days=target_date.weekday())
                    end_date = start_date + pd.Timedelta(days=6)
                    df_summary = df_summary[(df_summary['parsed_date'] >= start_date) & (df_summary['parsed_date'] <= end_date)]
                elif time_filter == 'month':
                    import calendar
                    start_date = target_date.replace(day=1)
                    _, last_day = calendar.monthrange(target_date.year, target_date.month)
                    end_date = target_date.replace(day=last_day)
                    df_summary = df_summary[(df_summary['parsed_date'] >= start_date) & (df_summary['parsed_date'] <= end_date)]
                elif time_filter == 'year':
                    start_date = target_date.replace(month=1, day=1)
                    end_date = target_date.replace(month=12, day=31)
                    df_summary = df_summary[(df_summary['parsed_date'] >= start_date) & (df_summary['parsed_date'] <= end_date)]

        # Convert numeric columns safely since Sheety might return mix types
        if 'NetValue' in df_summary.columns:
            df_summary['NetValue'] = pd.to_numeric(df_summary['NetValue'], errors='coerce').fillna(0)
        if 'Quantity' in df_summary.columns:
            df_summary['Quantity'] = pd.to_numeric(df_summary['Quantity'], errors='coerce').fillna(0)
        if 'LCValue' in df_summary.columns:
            df_summary['LCValue'] = pd.to_numeric(df_summary['LCValue'], errors='coerce').fillna(0)

        # Returns simple KPI data
        total_sales = df_summary['NetValue'].sum() if 'NetValue' in df_summary.columns else 0
        gross_sales = df_summary[df_summary['NetValue'] > 0]['NetValue'].sum() if 'NetValue' in df_summary.columns else 0
        total_returns = df_summary[df_summary['NetValue'] < 0]['NetValue'].sum() if 'NetValue' in df_summary.columns else 0
        
        total_qty = df_summary['Quantity'].sum() if 'Quantity' in df_summary.columns else 0
        total_orders = df_summary['VBELN'].nunique() if 'VBELN' in df_summary.columns else 0
        total_lc_value = df_summary['LCValue'].sum() if 'LCValue' in df_summary.columns else 0
        
        # Sales by Material Group
        sales_by_group = []
        if 'MatGrDes' in df_summary.columns and 'NetValue' in df_summary.columns:
            grouped = df_summary.groupby('MatGrDes')['NetValue'].sum().reset_index()
            # Sort by highest sales
            grouped = grouped.sort_values(by='NetValue', ascending=False).head(10)
            sales_by_group = grouped.to_dict(orient='records')
            
        # Top Customers
        top_customers = []
        if 'SoldToName1' in df_summary.columns and 'NetValue' in df_summary.columns:
            grouped_cust = df_summary.groupby('SoldToName1')['NetValue'].sum().reset_index()
            grouped_cust = grouped_cust.sort_values(by='NetValue', ascending=False).head(5)
            top_customers = grouped_cust.to_dict(orient='records')
            
        return {
            'total_sales': float(total_sales),
            'gross_sales': float(gross_sales),
            'total_returns': float(total_returns),
            'total_quantity': float(total_qty),
            'total_orders': int(total_orders),
            'total_lc_value': float(total_lc_value),
            'sales_by_group': sales_by_group,
            'top_customers': top_customers
        }

db = ExcelDB()
