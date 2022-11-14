import pandas as pd


def main():
    file1 = pd.read_json('file1.json')
    file2 = pd.read_json('file2.json')

    if len(file1.columns.difference(file2.columns)) == 0:
        data = pd.concat([file1, file2], axis=0)
        data.reset_index(drop=True,inplace=True)
        data.to_json('output.json',orient = 'columns',indent=4)




if __name__ == "__main__":
    main()