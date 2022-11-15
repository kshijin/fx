import pandas as pd
import os
import glob

# generator object to read the files from the folder
class Reader:
    def __init__(self,fn):
        self.files = glob.glob(os.path.join(fn, "*.csv"))
    

    def __iter__(self):
        #TODO handle large files
        for csv_file_name in self.files:
            yield pd.read_csv(csv_file_name)
    