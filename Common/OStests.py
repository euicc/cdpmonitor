import subprocess
import os
import csv
import time
import datetime
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings
from termcolor import colored
ts = time.time()


timestamp = datetime.datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S')


filename = "results/result.csv"


def checkProcess():
 output = subprocess.check_output(['ps', '-A'])
 processes  = ["httpd","openhab2","sshd"]
 for i in processes:
  if i in output:
    print(i + " is up an running!")
  else:
    print(i+ " is not running!")

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
	elif used_space == "85%":
        	print "WARNING - %s of disk space used." % used_space
	elif used_space > "85%":
        	print "CRITICAL - %s of disk space used." % used_space
	else:
        	print "UKNOWN - %s of disk space used." % used_space

def usedMemory():
	tot_m, used_m, free_m = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
	swap_t, swap_u, swap_f = map(int, os.popen('free -t -m').readlines()[-2].split()[1:])

	mem_critic = settings.config['Memory Threshold']['CRITICAL']
	mem_major = settings.config['Memory Threshold']['MAJOR']
	mem_warning = settings.config['Memory Threshold']['WARNING']

	swap_percent = swap_u*100/swap_t

	if swap_percent < int(mem_warning) :
        	print colored("--- SWAP usage OK --- ",'green')
        	print("SWAP Total:" + str(swap_t) + " Usage:" + str(swap_u) + " Free:" + str(swap_f) + " Used:" + str(swap_percent) + "%")
	elif swap_percent >= int(mem_warning) and swap_percent < int(mem_major):
        	print colored("--- SWAP usage NOK --- in Warning alarm", 'yellow')
        	print("SWAP Total:" + str(swap_t) + " Usage:" + str(swap_u) + " Free:" + str(swap_f) + " Used:" + str(swap_percent) + "%")
	elif swap_percent >= int(mem_major) and swap_percent < int(mem_critic):
        	print colored("--- SWAP usage NOK --- in Major alarm", 'magenta')
        	print("SWAP Total:" + str(swap_t) + " Usage:" + str(swap_u) + " Free:" + str(swap_f) + " Used:" + str(swap_percent) + "%")
	elif swap_percent >= int(mem_critic):
        	print colored("--- SWAP usage NOK --- in Critical alarm", 'red')
        	print("SWAP Total:" + str(swap_t) + " Usage:" + str(swap_u) + " Free:" + str(swap_f) + " Used:" + str(swap_percent) + "%")

	mem_percent =  int(used_m*100/tot_m)

	if mem_percent < int(mem_warning):
        	print colored("--- MEMORY usage OK --- ",'green')
        	print("MEMORY Total:" + str(tot_m) + " Usage:" + str(used_m) + " Free:" + str(free_m) + " Used:" + str(mem_percent) + "%")
	elif mem_percent >= int(mem_warning) and mem_percent < int(mem_major):
        	print colored("--- MEMORY usage NOK --- in Warning alarm", 'yellow')
        	print("MEMORY Total:" + str(tot_m) + " Usage:" + str(used_m) + " Free:" + str(free_m) + " Used:" + str(mem_percent) + "%")
	elif mem_percent >= int(mem_major) and mem_percent < int(mem_critic):
        	print colored("--- MEMORY usage NOK --- in Major alarm", 'magenta')
        	print("MEMORY Total:" + str(tot_m) + " Usage:" + str(used_m) + " Free:" + str(free_m) + " Used:" + str(mem_percent) + "%")
	elif mem_percent >= int(mem_critic):
        	print colored("--- MEMORY usage NOK --- in Critical alarm", 'red')
        	print("MEMORY Total:" + str(tot_m) + " Usage:" + str(used_m) + " Free:" + str(free_m) + " Used:" + str(mem_percent) + "%")

