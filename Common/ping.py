import subprocess
import os
import json
from easydict import EasyDict as edict
import time
import datetime

ts = time.time()


d = edict({'tests':{'testName':'pingtest','result':{}}})
d.tests.timestamp = datetime.datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S')


filename = "data.json"


#print("Reading %s" % filename)
#try:
#    with open(filename, "r") as fp:
#        d = json.load(fp)
#    print(d)
#except IOError:
#    print("Could not read file, starting from scratch")

#runtime = datetime.datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S')



#d["tests"].append(dict(timestamp=runtime))

with open('servers.txt', 'r') as f:
        for ip in f:
            result=subprocess.Popen(["ping", "-c", "1", "-n", "-W", "2",    ip],stdout=f, stderr=f).wait()
            if result:
                print(ip, "inactive")
		d.tests.result[ip] = {
                   "result": {
                             "name": "ping",
                             "ip":ip,
                             "result":result
                              }
            	}
		with open(filename, "w") as fp:
    			json.dump(d, fp,indent=4)
            else:
                print(ip, "active")
		d.tests.result[ip] = {
                   "result": {
                             "name": "ping",
                             "ip":ip,
                             "result":result
                              }
           	}
		with open(filename, "w") as fp:
    			json.dump(d, fp,indent = 4)
