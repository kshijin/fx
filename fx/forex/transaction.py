import requests
import os
from .db import Forex
from .parser import Reader

class ForexTransaction:
    """
    Record the transfer from folder to database with conversion rate

    Args:
    @params folder_name: foldername to read files

    Attributes:
    folder_name: show the folder name
    show_data: print all transaction from db to console 
    read_data: read the files and save to db with convertion rate 
    """
    def __init__(self,folder_name) -> None:
        self.folder_name = folder_name

    def read_data(self) -> None:
        # Read files form the folder
        rd = Reader(self.folder_name)
        for file in rd:
            # get column name for each column
            from_cur_c = self._get_from_cur(file)
            to_cur_c = self._get_to_cur(file)
            amd_c = self._get_amount(file)
            op = []
            for _, row in file.iterrows():
                #calculate convertion rate 
                result = ForexTransaction.caculate_fx(row[from_cur_c],row[to_cur_c],row[amd_c])
                op.append({
                    'from_cur': row[from_cur_c],
                    'to_cur':row[to_cur_c],
                    'amount':row[amd_c],
                    'rate':result.get('info',{}).get('rate'),
                    'transation_date':result.get('info',{}).get('timestamp'),
                    'result' : result.get('result')
                })
            # excuiting bulk insert
            q=Forex.insert_many(op)
            q.execute()
                
    def show_data(self)-> None:
        """
        print all transaction from db to console 
        """
        rows=Forex.select()
        for row in rows:
            print (f"from_cur: {row.from_cur} to_cur: {row.to_cur} amount: {row.amount} rate: {row.rate}")

    def _get_from_cur(self,pd) -> str:
        """
        get the from currency column name dataframe
        """
        return pd.columns.intersection(['SourceCurrency','Currrency1','CurrencyFrom']).any()
           

    def _get_to_cur(self,pd) -> str:
        """
        get the to currency column name dataframe
        """
        return pd.columns.intersection(['DestinationCuttency','Currrency2','CurrencyTo']).any()

    def _get_amount(self,pd) -> str:
        """
        get the amount column name dataframe
        """
        return pd.columns.intersection(['SourceAmount','ScrAmount','SourceFrom']).any()

    @staticmethod
    def caculate_fx(from_cur,to_cur,amount) -> dict:  
        """
        get conversion rate
        @parms from_cur: from currency
        @parms to_cur: to currency
        @pams amount: transfer amount
        """  
        # get the api key from env 
        headers = {
            'apikey': os.getenv('APIKEY')
        }
        # construct the url
        url = f'https://api.apilayer.com/fixer/convert?from={from_cur}&to={to_cur}&amount={amount}'
        # get the response from APi
        # TODO handle exception 
        response = requests.get(url, headers=headers)
        return response.json()
