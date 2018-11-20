import time
import modules.pexpect

def jmx():
	connection = "localhost:3993"
	connection_timeout = 2

	jmxterm = modules.pexpect.spawn("java -jar jmxterm-1.0-alpha-4-uber.jar")
	jmxterm.expect_exact("$>") # got prompt, we can continue
	jmxterm.sendline("open " + connection)
	jmxterm.expect_exact("#Connection to "+connection+" is opened", connection_timeout)

	jmxterm.sendline("get -d Catalina -b name=http-80,type=ThreadPool currentThreadCount")

	response_lines = []
	response_lines.append(jmxterm.readline())
	response_lines.append(jmxterm.readline())
	response_lines.append(jmxterm.readline())
	response_lines.append(jmxterm.readline())

	result = response_lines[3].replace(";"," ").strip().split(" ")
	del result[1]
	name,value = result

	print "["+time.ctime()+"]", name, "=", value
	jmxterm.sendline("quit")
