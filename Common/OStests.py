import subprocess
import os
import csv
import time
from time import sleep
import datetime
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings
from modules.termcolor.termcolor import colored
from modules import psutil
ts = time.time()


timestamp = datetime.datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S')


filename = "results/result.csv"

if "check_output" not in dir( subprocess ): # duck punch it in!
    def f(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd)
        return output
    subprocess.check_output = f

def checkProcess():
 testname= "checkProcess"
 output = subprocess.check_output(['ps', '-A'])
 processes  = ["httpd","openhab2","sshd"]
 for i in processes:
  if i in output:
    print(i + " is up an running!")
    logTestResult(testname,i,"is up an running!")
  else:
    print(i+ " is not running!")
    logTestResult(testname,i,"is not running!")

def pingAllHosts():
  testname="ping"
  with open('servers.txt', 'r') as f:
      lines = f.readlines()
      lines = [line.rstrip('\n') for line in open('servers.txt')]   
      for ip in lines:
            result=subprocess.Popen(["ping", "-c", "1", "-n", "-W", "2",    ip],stdout=f, stderr=f).wait()
            if result:
                print(ip, "inactive")
		logTestResult(testname,ip,"inactive")
            else:
                print(ip, "active")
		logTestResult(testname,ip,"iactive")

def usedSpace():
    testname ="usedSpace"
    diskSpace_critic = settings.config['DiskSpaceThreshold']['CRITICAL']
    diskSpace_major = settings.config['DiskSpaceThreshold']['MAJOR']
    diskSpace_warning = settings.config['DiskSpaceThreshold']['WARNING']
    partitions= os.popen("df -h | grep -v Filesystem | awk '{print $1}'").readlines()
    for partition in partitions:
	command ="df -h " + partition.strip('\n') + " | grep -v Filesystem | awk '{print $5}'"
	used_space = os.popen(command).readline().strip('%\n')
	print (used_space)
    	if (used_space <= diskSpace_warning):
        	print (partition.strip('\n') + " OK " + used_space + "% of disk space used.")
        	logTestResult(testname,used_space,"OK")
    	elif (used_space > diskSpace_warning and used_space <= diskSpace_critic):
       		print(partition.strip('\n') + " WARNING - " + used_space +"% of disk space used.")
		logTestResult(testname,used_space,"WARNING")
    	elif (used_space > diskSpace_critic):
       		print colored(partition.strip('\n') + " CRITICAL - %s of disk space used." % used_space,'red')
		logTestResult(testname,used_space,"CRITICAL")
    	else:
       		print(partition .strip('\n') + " UKNOWN - %s of disk space used." % used_space)
		logTestResult(testname,used_space,"UKNOWN")

def usedMemory():
	testname="usedMemory"
	tot_m, used_m, free_m = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
	swap_t, swap_u, swap_f = map(int, os.popen('free -t -m').readlines()[-2].split()[1:])

	mem_critic = settings.config['MemoryThreshold']['CRITICAL']
	mem_major = settings.config['MemoryThreshold']['MAJOR']
	mem_warning = settings.config['MemoryThreshold']['WARNING']

	if (swap_t !=0):
                swap_percent = swap_u*100/swap_t
                if swap_percent < int(mem_warning) :
                        print colored("--- SWAP usage OK --- ",'green')
                        print("SWAP Total:" + str(swap_t) + " Usage:" + str(swap_u) + " Free:" + str(swap_f) + " Used:" + str(swap_percent) + "%")
                        logTestResult(testname,"SWAP Total:" + str(swap_t) + " Usage:" + str(swap_u) + " Free:" + str(swap_f) + " Used:" + str(swap_percent) + "%","")
                elif swap_percent >= int(mem_warning) and swap_percent < int(mem_major):
                        print colored("--- SWAP usage NOK --- in Warning alarm", 'yellow')
                        print("SWAP Total:" + str(swap_t) + " Usage:" + str(swap_u) + " Free:" + str(swap_f) + " Used:" + str(swap_percent) + "%")
                        logTestResult(testname,"SWAP Total:" + str(swap_t) + " Usage:" + str(swap_u) + " Free:" + str(swap_f) + " Used:" + str(swap_percent) + "%","")
                elif swap_percent >= int(mem_major) and swap_percent < int(mem_critic):
                        print colored("--- SWAP usage NOK --- in Major alarm", 'magenta')
                        print("SWAP Total:" + str(swap_t) + " Usage:" + str(swap_u) + " Free:" + str(swap_f) + " Used:" + str(swap_percent) + "%")
                        logTestResult(testname,"SWAP Total:" + str(swap_t) + " Usage:" + str(swap_u) + " Free:" + str(swap_f) + " Used:" + str(swap_percent) + "%","")
                elif swap_percent >= int(mem_critic):
                        print colored("--- SWAP usage NOK --- in Critical alarm", 'red')
                        print("SWAP Total:" + str(swap_t) + " Usage:" + str(swap_u) + " Free:" + str(swap_f) + " Used:" + str(swap_percent) + "%")
                        logTestResult(testname,"SWAP Total:" + str(swap_t) + " Usage:" + str(swap_u) + " Free:" + str(swap_f) + " Used:" + str(swap_percent) + "%","")
        else:
                swap_percent = swap_u
                print colored("--- SWAP Not initialized --- ",'green')
                print("SWAP Total:" + str(swap_t) + " Usage:" + str(swap_u) + " Free:" + str(swap_f) + " Used:" + str(swap_percent) + "%")
                logTestResult(testname,"SWAP Total:" + str(swap_t) + " Usage:" + str(swap_u) + " Free:" + str(swap_f) + " Used:" + str(swap_percent) + "%","")


	mem_percent =  int(used_m*100/tot_m)

	if mem_percent < int(mem_warning):
        	print colored("--- MEMORY usage OK --- ",'green')
        	print("MEMORY Total:" + str(tot_m) + " Usage:" + str(used_m) + " Free:" + str(free_m) + " Used:" + str(mem_percent) + "%")
		logTestResult(testname,"MEMORY Total:" + str(tot_m) + " Usage:" + str(used_m) + " Free:" + str(free_m) + " Used:" + str(mem_percent) + "%","")
	elif mem_percent >= int(mem_warning) and mem_percent < int(mem_major):
        	print colored("--- MEMORY usage NOK --- in Warning alarm", 'yellow')
        	print("MEMORY Total:" + str(tot_m) + " Usage:" + str(used_m) + " Free:" + str(free_m) + " Used:" + str(mem_percent) + "%")
		logTestResult(testname,"MEMORY Total:" + str(tot_m) + " Usage:" + str(used_m) + " Free:" + str(free_m) + " Used:" + str(mem_percent) + "%","")
	elif mem_percent >= int(mem_major) and mem_percent < int(mem_critic):
        	print colored("--- MEMORY usage NOK --- in Major alarm", 'magenta')
        	print("MEMORY Total:" + str(tot_m) + " Usage:" + str(used_m) + " Free:" + str(free_m) + " Used:" + str(mem_percent) + "%")
		logTestResult(testname,"MEMORY Total:" + str(tot_m) + " Usage:" + str(used_m) + " Free:" + str(free_m) + " Used:" + str(mem_percent) + "%","")
	elif mem_percent >= int(mem_critic):
        	print colored("--- MEMORY usage NOK --- in Critical alarm", 'red')
        	print("MEMORY Total:" + str(tot_m) + " Usage:" + str(used_m) + " Free:" + str(free_m) + " Used:" + str(mem_percent) + "%")
		logTestResult(testname,"MEMORY Total:" + str(tot_m) + " Usage:" + str(used_m) + " Free:" + str(free_m) + " Used:" + str(mem_percent) + "%","")

def logTestResult(testname,data,state):
    with open(filename, 'a') as csvfile:
        resultwriter = csv.writer(csvfile, delimiter=',')
        resultwriter.writerow([testname,timestamp,data,state])


class GetCpuLoad(object):
    def __init__(self, percentage=True, sleeptime = 1):
        self.percentage = percentage
        self.cpustat = '/proc/stat'
        self.sep = ' ' 
        self.sleeptime = sleeptime

    def getcputime(self):
        cpu_infos = {} 
        with open(self.cpustat,'r') as f_stat:
            lines = [line.split(self.sep) for content in f_stat.readlines() for line in content.split('\n') if line.startswith('cpu')]

            for cpu_line in lines:
                if '' in cpu_line: cpu_line.remove('')#remove empty elements
                cpu_line = [cpu_line[0]]+[float(i) for i in cpu_line[1:]]#type casting
                cpu_id,user,nice,system,idle,iowait,irq,softrig,steal,guest,guest_nice = cpu_line

                Idle=idle+iowait
                NonIdle=user+nice+system+irq+softrig+steal

                Total=Idle+NonIdle
                cpu_infos.update({cpu_id:{'total':Total,'idle':Idle}})
            return cpu_infos

    def getcpuload(self):
        start = self.getcputime()
        sleep(self.sleeptime)
        stop = self.getcputime()

        cpu_load = {}

        for cpu in start:
            Total = stop[cpu]['total']
            PrevTotal = start[cpu]['total']

            Idle = stop[cpu]['idle']
            PrevIdle = start[cpu]['idle']
            CPU_Percentage=((Total-PrevTotal)-(Idle-PrevIdle))/(Total-PrevTotal)*100
            cpu_load.update({cpu: round(CPU_Percentage,2)})
        return cpu_load


def cpuUsage():
    x = GetCpuLoad()
    cpu_info = x.getcpuload()
    usage = cpu_info['cpu']
    testname="cpuUsage"

    cpuUsage_critic = settings.config['CpuThreshold']['CRITICAL']
    cpuUsage_major = settings.config['CpuThreshold']['MAJOR']
    cpuUsage_warning = settings.config['CpuThreshold']['WARNING']

    if usage < int(cpuUsage_warning):
	print colored("--- CPU USAGE OK --- ",'green')
	print cpu_info
        logTestResult(testname,cpu_info,"OK")
    elif usage >= int(cpuUsage_warning) and usage < int(cpuUsage_major):
	print colored("--- CPU USAGE NOK --- ",'yellow')
        print cpu_info
        logTestResult(testname,cpu_info,"WARNING")
    elif usage >= int(cpuUsage_major) and usage < int(cpuUsage_critic):
        print colored("--- CPU USAGE NOK --- ",'magenta')
        print cpu_info
        logTestResult(testname,cpu_info,"MAJOR")
    elif usage >= int(cpuUsage_critic):
        print colored("--- CPU USAGE NOK --- ",'red')
        print cpu_info
        logTestResult(testname,cpu_info,"CRITIC")

def systemInfo():
	print colored("System information",'magenta')
	print ("Nb of CPU: "+ str(psutil.cpu_count()))
