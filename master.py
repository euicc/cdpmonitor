import os
from modules.termcolor.termcolor import colored
import json
import settings
from Common import OStests

#with open('config.json', 'r') as f:
#    config = json.load(f)

customTests=[]
results = []
testdir = settings.config['COMMON']['NAME'] # 'product'
tests=settings.config['TESTS'] #'tests to be run'
customTestsDir='CustomTests'


print colored("=============Predefined tests============",'magenta')
print('\n')
for test in tests:

	
	print colored("==============="+test+"==================",'yellow')
	run="OStests."+test+"()"
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



