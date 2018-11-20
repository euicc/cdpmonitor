import os
from modules.termcolor.termcolor import colored
import json
import helpers
from Common import OStests

#with open('config.json', 'r') as f:
#    config = json.load(f)

customTests=[]
results = []
testdir = helpers.config['COMMON']['NAME'] # 'product'

#check for product and select appropriated tests
platform=helpers.config['PLATFORM']['NAME']
if (platform=="HDM"):
	platformtests=helpers.config["HDMTESTS"]
	from HDM import HDM
if (platform=="CDP"):
	platformtests=helpers.config["CDPTESTS"]
	from CDP import CDP
if (platform =="HAL"):
	platformtests=helpers.config["HALTESTS"]
	from HAL import HAL
commontests=helpers.config['COMMONTESTS'] #'tests to be run'
customTestsDir='CustomTests'


print colored("=============Common tests============",'magenta')
print('\n')
for test in commontests:

	
	print colored("==============="+test+"==================",'yellow')
	run="OStests."+test+"()"
	#print (run)
	exec(run)
	#print colored("==============================================================",'yellow')
	print('\n')


print colored("=============Platform specific tests============",'magenta')
print('\n')


if (len(platformtests)==0):
	print colored("No tests to run",'red')
else:
	for platformtest in platformtests:	
        	print colored("==============="+platformtest+"==================",'yellow')
        	run=platform+"."+platformtest+"()"
	        #print (run)
        	exec(run)
	        #print colored("==============================================================",'yellow')
	        print('\n')


print colored(    "=================Custom tests============",'magenta')
print('\n')

print os.listdir(customTestsDir)
for files in os.listdir(customTestsDir):
  if files.endswith('.py'):
      results.append(files)

for result in results:
		os.system('python ' + customTestsDir + "/"  + result)



