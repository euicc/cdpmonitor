import subprocess
import os
import csv
import time
import datetime
import sys
ts = time.time()


timestamp = datetime.datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S')


filename = "results/result.csv"

def pingAllHosts():
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


def usedSpace():
	used_space=os.popen("df -h / | grep -v Filesystem | awk '{print $5}'").readline().strip()

	if used_space < "85%":
        	print "OK - %s of disk space used." % used_space
        	sys.exit(0)
	elif used_space == "85%":
        	print "WARNING - %s of disk space used." % used_space
        	sys.exit(1)
	elif used_space > "85%":
        	print "CRITICAL - %s of disk space used." % used_space
        	sys.exit(2)
	else:
        	print "UKNOWN - %s of disk space used." % used_space
        	sys.exit(3)

