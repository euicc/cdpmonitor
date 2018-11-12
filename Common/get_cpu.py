import os

def getCPU():
	CPU_Pct=str(round(float(os.popen('''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline()),2))	
  	return CPU_Pct


x = getCPU()
'''
while True:
        try:
            data = getCPU()
            print data
        except KeyboardInterrupt:
            sys.exit("Finished")     
'''

#print results
print("CPU Usage = " + x)
