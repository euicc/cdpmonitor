import os
from modules.termcolor.termcolor import colored
import json
import settings
from Common import OStests

#with open('config.json', 'r') as f:
#    config = json.load(f)

results = []
testdir = settings.config['COMMON']['NAME'] # 'product'
tests=["usedMemory","pingAllHosts","usedSpace","checkProcess"]
#print os.listdir(testdir)
#for f in os.listdir(testdir):
#  if f.endswith('.py'):
#      results.append(f)
for test in tests:

	print colored("=================================",'blue')
	#os.system('python ' + testdir + "/"  + i)
	run="OStests."+test+"()"
	#print (run)
	exec(run)
	print colored("=================================",'blue')
