from utils import *

# logging level: NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
logger = logging.getLogger()
logger.setLevel(logging.INFO)

LIST_LIST_LINE = [
    ["0"], 
    ["5", "1 3", "2 4", "4 6", "26 29", "5 2"],
    ["2", "4 6", "23 24"],
    ["1", "20 23", "22 5"],
    ["9", "4 6", "8 10", "10 14", "9 15", "18 20", "19 23", "23 3", "7 8", "16 17", "22 2", "8 10", "10 14"],
]

def main():
    for list_line in LIST_LIST_LINE:
        process_list_line(list_line)

if __name__ == '__main__':
    main()  # Standard boilerplate to call the main() function to begin the program.
