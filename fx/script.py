import sys
import time
from forex.transaction import ForexTransaction


def main(folder_name):
    if len(folder_name) == 1:
        fx = ForexTransaction(folder_name[0])
        fx.read_data()
        fx.show_data()
    else:
        print("unsupported args")

if __name__ == "__main__":
    start_time = time.time()
    main(sys.argv[1:]) 
    print("--- %s seconds ---" % (time.time() - start_time))
