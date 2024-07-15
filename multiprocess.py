import csv
import os
import multiprocessing
from watchdog import watchprocess
import logging
import argparse

logging.basicConfig(filename='course_player.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="课程播放器多线程自动化脚本")
    parser.add_argument("--filename", '-f', help="文件名称", default='accounts.csv')
    args = parser.parse_args()

    current_working_directory = os.getcwd()
    accounts_file_path = args.filename 

    try:
        with open(accounts_file_path, 'r') as file:
            reader = csv.reader(file)
            processes = []
            for row in reader:
                username, password = row
                process = multiprocessing.Process(target=watchprocess, args=(username, password))
                process.start()
                processes.append(process)

    except FileNotFoundError:
        print(f"The file {accounts_file_path} does not exist.")
    except csv.Error as e:
        print(f"Error reading CSV file at line {reader.line_num}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
