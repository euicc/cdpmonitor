import sys, os, subprocess
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import helpers
from modules.termcolor.termcolor import colored
import subprocess

import MySQLdb


def run_cmd(args_list):
#	print('Running system command: "{0}"'.format(' '.join(args_list)))
	proc = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	s_output, s_err = proc.communicate()
	s_return =  proc.returncode
	return s_return, s_output, s_err 


def hdfs_used():
	testname = "hdfs_used"
	cmd = ['sudo', '-u', 'hdfs', 'hdfs', 'dfs', '-df', '-h', '/']
	(ret, out, err)= run_cmd(cmd)
	if ret != 0:
		print('Cannot run the command: ' + ' '.join(cmd))
	elif ret == 0:
		hdfs_usage = out.split('\n')[1:2][0].split()[-1][0].strip('%')
		hdfs_info = "DFS used  = " + hdfs_usage + "%"
    
		hdfsUsage_critic = helpers.config['HdfsThreshold']['CRITICAL']
		hdfsUsage_major = helpers.config['HdfsThreshold']['MAJOR']
		hdfsUsage_warning = helpers.config['HdfsThreshold']['WARNING']

		if int(hdfs_usage) < int(hdfsUsage_warning):
			print colored("--- hdfs USAGE OK --- ",'green')
			print hdfs_info
			helpers.logTestResult(testname,hdfs_info,"OK")
		elif int(hdfs_usage) >= int(hdfsUsage_warning) and int(hdfs_usage) < int(hdfsUsage_major):
			print colored("--- hdfs USAGE NOK --- ",'yellow')
			print hdfs_info
			helpers.logTestResult(testname,hdfs_info,"WARNING")
		elif int(hdfs_usage) >= int(hdfsUsage_major) and int(hdfs_usage) < int(hdfsUsage_critic):
			print colored("--- hdfs USAGE NOK --- ",'magenta')
			print hdfs_info
 		       	helpers.logTestResult(testname,hdfs_info,"MAJOR")
		elif int(hdfs_usage) >= int(hdfsUsage_critic):
			print colored("--- hdfs USAGE NOK --- ",'red')
			print hdfs_info
			helpers.logTestResult(testname,hdfs_info,"CRITIC")
	
	
#hdfs_used()


def check_oozie():
	testname = "check_oozie"
	print("--- Checking oozie jobs status ---")
	db = MySQLdb.connect(host="localhost", user="oozie", passwd="asdfasdf", db="oozie")  
	curr = db.cursor()

	curr.execute("select distinct app_name,status from WF_JOBS where date(start_time) = date(now()) ;")
	rows = curr.fetchall()
	db.close()

	for t in rows:
	   if t[1] in ['FAILED','KILLED','RUNNING']:
		print("Job " + t[0] + " is in " + t[1] + " state " )
		



#check_oozie()	

