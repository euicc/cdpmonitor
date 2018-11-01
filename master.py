import os
from termcolor import colored
import json

with open('config.json', 'r') as f:
    config = json.load(f)

results = []
testdir = config['COMMON']['NAME'] # 'product'
print os.listdir(testdir)
for f in os.listdir(testdir):
  if f.endswith('.py'):
      results.append(f)

for i in results:
	print colored("=================================",'blue')
	os.system('python ' + testdir + "/"  + i)
	print colored("=================================",'blue')
