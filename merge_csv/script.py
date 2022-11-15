import pandas as pd
import numpy as np
import os
import glob


def create_sample(num:int) -> None:
    '''
    create sample csv file with 1000000 row with random data
    @param num: number of files to create

    '''
    n_rows = 1000000
    n_cols = 20
    # creating pandas dataframe with 20 columns and 1000000 rows
    df = pd.DataFrame(np.random.randint(0, 100, size=(n_rows, n_cols)), columns=['col%d' % i for i in range(n_cols)])
    for each in range(num):
        # createing csv file with large data
        df.to_csv(f'sales_records/file{each}.csv',index=False)


def merge_csv() -> None:
    """
    merge csv of large data from the folder sales_records
    """
    SIZE = 200000
    # get all csv file in the folders
    files = glob.glob(os.path.join('sales_records' , "*.csv"))
    for csv_file_name in files:
        # read part of the csv 
        chunk_container = pd.read_csv(csv_file_name, chunksize=SIZE)
        for chunk in chunk_container:
            chunk.to_csv('sales_records/file-output.csv', mode="a", index=False)
    


if __name__ == "__main__":
    create_sample(5)
    merge_csv()