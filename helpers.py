# to keep the global variable
import json
import csv
import os
import time
from time import sleep
import datetime
filename = "results/result.csv"
ts = time.time()
timestamp = datetime.datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S')

with open('config.json', 'r') as f:
    config = json.load(f)

def logTestResult(testname,data,state):
    with open(filename, 'a') as csvfile:
        resultwriter = csv.writer(csvfile, delimiter=',')
        resultwriter.writerow([testname,timestamp,data,state])
