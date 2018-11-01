
import subprocess
output = subprocess.check_output(['ps', '-A'])
processes  = ["httpd","openhab2","sshd"]
for i in processes:
  if i in output:
    print(i + " is up an running!")
  else:
    print(i+ " is not running!")
