import sys
import time
from forex.transaction import ForexTransaction


def main(folder_name):
    """
    read all file from folder and output transaction details
    @param folder_name: name of folder to read the files
    """
    if len(folder_name) == 1:
        fx = ForexTransaction(folder_name[0])
        fx.read_data()
        fx.show_data()
    else:
        print("unsupported args")

if __name__ == "__main__":
    start_time = time.time()
    # reading cmd line args
    main(sys.argv[1:]) 
    print("--- %s seconds ---" % (time.time() - start_time))
