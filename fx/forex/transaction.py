import requests
import os
from .db import Forex
from .parser import Reader

class ForexTransaction:
    def __init__(self,folder_name) -> None:
        self.folder_name = folder_name

    def read_data(self):
        rd = Reader(self.folder_name)
        for file in rd:
            from_cur_c = self.get_from_cur(file)
            to_cur_c = self.get_to_cur(file)
            amd_c = self.get_amount(file)
            file.columns.isin(['A', 'C'])
            op = []
            for _, row in file.iterrows():
                result = ForexTransaction.caculate_fx(row[from_cur_c],row[to_cur_c],row[amd_c])
                op.append({
                    'from_cur': row[from_cur_c],
                    'to_cur':row[to_cur_c],
                    'amount':row[amd_c],
                    'rate':result.get('info',{}).get('rate'),
                    'transation_date':result.get('info',{}).get('timestamp'),
                    'result' : result.get('result')
                })
            q=Forex.insert_many(op)
            q.execute()
                
    def show_data(self):
        rows=Forex.select()
        for row in rows:
            print (f"from_cur: {row.from_cur} to_cur: {row.to_cur} amount: {row.amount} rate: {row.rate}")

    def get_from_cur(self,pd):
        return pd.columns.intersection(['SourceCurrency','Currrency1','CurrencyFrom']).any()
           

    def get_to_cur(self,pd):
        return pd.columns.intersection(['DestinationCuttency','Currrency2','CurrencyTo']).any()

    def get_amount(self,pd):
        return pd.columns.intersection(['SourceAmount','ScrAmount','SourceFrom']).any()

    @staticmethod
    def caculate_fx(from_cur,to_cur,amount):    
        headers = {
            'apikey': os.getenv('APIKEY')
        }
        url = f'https://api.apilayer.com/fixer/convert?from={from_cur}&to={to_cur}&amount={amount}'
        response = requests.get(url, headers=headers)
        return response.json()
    
    def insert_record(self):
        pass
