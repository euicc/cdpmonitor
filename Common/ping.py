import subprocess
import os
import csv
import time
import datetime

ts = time.time()


timestamp = datetime.datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S')


filename = "results/result.csv"


with open('servers.txt', 'r') as f:
      lines = f.readlines()
      lines = [line.rstrip('\n') for line in open('servers.txt')]   
      for ip in lines:
            result=subprocess.Popen(["ping", "-c", "1", "-n", "-W", "2",    ip],stdout=f, stderr=f).wait()
            if result:
                print(ip, "inactive")
		with open(filename, 'a') as csvfile:
    			resultwriter = csv.writer(csvfile, delimiter=',')
    			resultwriter.writerow(["ping",timestamp,ip,result])
            else:
                print(ip, "active")
		with open(filename, 'a') as csvfile:
                	resultwriter = csv.writer(csvfile, delimiter=',')
                	resultwriter.writerow(["ping",timestamp,ip,result])

