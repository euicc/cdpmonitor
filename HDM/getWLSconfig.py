#!/usr/bin/python
# Script that captures HDM configuration from config.xml file. 
# version 1.2


#Import portion
import platform, sys, subprocess, ConfigParser, datetime, os, getopt, itertools, time, socket

global scriptversion 
scriptversion = '1.1'

# Print the usage of the script in case arguments are incorrect
def usage():
	print 'usage: python ' + sys.argv[0] + ' [option]'
	print 'Options and arguments:'
	print '-h 					:print this help message and exit (also --help)'
#	print '-o 					:directory to store the output (also --output). Default is current directory'
	print '-a 					:active configuration (also --active). Default is /opt/hdm/domains/HDMDomain/config'
	print '-f 					:config.xml file location (also --file). Default is current directory'


# Checking the input arguments and setting defaults
def checkInput():
	try:
		optlist, args = getopt.getopt(sys.argv[1:], 'hafo:', ['help','active','file'])
	except getopt.GetoptError as err:
		# print help information and exit:
		print str(err)
		usage()
		sys.exit(2)

	global WLSconfigdirectory
	WLSconfigdirectory = '.'
	global outputdirectory
	outputdirectory = '.'
	# Checking the options and arguments:
	# First Check if nothing is provided 
	if not optlist:
		usage()
		sys.exit(2)
	# If something is provided as arguments then we check further
	for opt, arg in optlist:
		if opt in ('-h', '--help'):
			usage()
			sys.exit(0)
		elif opt in ('-o','--output'):
			outputdirectory = arg
		elif opt in ('-a','--active'):
			readConfig()
			print '\nReading active configuration ...\n'
			print '================================================================================='
			# Define directory based on data.ini files inputs
			WLSconfigdirectory = HDM_HOME + '/domains/' + HDM_DOMAIN + '/config'
			
			if not os.path.isdir(WLSconfigdirectory):
				errHandler('4')
			elif not os.path.isfile(WLSconfigdirectory + '/config.xml'):
				errHandler('5')
				
			getWLSconfig()
			
		elif opt in ('-f','--file'):
			#readConfig()
			print '\nReading configuration from file ...\n'
			print '================================================================================='
			getWLSconfig()
		else:
			usage()
			sys.exit(2)


# Reading the data.ini file to get configuration variables for the script
def readConfig():
	if not os.path.isfile('./data.ini'):
		errHandler('3')
		
	Config = ConfigParser.ConfigParser('')
	Config.read('data.ini')
	global HDM_HOME
	HDM_HOME=Config.get('ApplicationDetails','HDM_HOME')
	global HDM_DOMAIN
	HDM_DOMAIN=Config.get('ApplicationDetails','HDM_DOMAIN')


# Use curl to make requests from Python
import httplib
def curl(*args):
    command = 'curl -s -i --insecure'.split() + list(args)
    pipe = subprocess.Popen(command, stdin=None, stdout=subprocess.PIPE,
                            stderr=sys.stderr)

    # HTTPResponse expects a socket, then calls `makefile()` on it.
    class mock_socket(object):
        def makefile(self, *args, **kwargs):
            return pipe.stdout

    try:
		response = httplib.HTTPResponse(mock_socket())
		response.begin()  # read HTTP headers and status line.
		return response
    except:
		#response = null
	
	return response
	

def getWLSconfig():
	global now
	now = datetime.datetime.now()
	print '\n1. Gathering WLS config file config.xml'
	print '-'*100
	# Define the output file
	destination_file_name = outputdirectory + '/wls_config'
	destinationfile = open(destination_file_name,'w')
	# Write the file
	destinationfile.write('1. Time the script was launched is: ' + now.strftime('%c') + '\n')

	# Open the config.xml file to read
	configXMLfile = WLSconfigdirectory + '/config.xml'
	configXML = open(configXMLfile, 'r')
	
	print 'WLS config directory: ' + WLSconfigdirectory
	print 'Config file: ' + configXMLfile
	print("Last modified: %s" % time.ctime(os.path.getmtime(configXMLfile)))
	
	import xml.etree.ElementTree as ET
	tree = ET.parse(configXMLfile)
	root = tree.getroot()

	print '\n'
	print '\n2. DOMAIN configuration ...\n'
	print '-'*100
	domainname = root.find('{http://xmlns.oracle.com/weblogic/domain}name').text
	print '\nDOMAIN: ', domainname
	
	print ('\n\t{0:45}\t\t{1:35}' .format('Administration Server Name', 'Administration port'))
	print '\t', '='*45, '\t\t', '='*35 
	adminservername = root.find('{http://xmlns.oracle.com/weblogic/domain}admin-server-name').text
	print ('\t{0:45}\t\t' .format(adminservername)),
	
	if root.find('{http://xmlns.oracle.com/weblogic/domain}administration-port') is not None:
		administrationport = root.find('{http://xmlns.oracle.com/weblogic/domain}administration-port').text
		print ('{0:35}' .format(administrationport))
	else:
		print ('{0:35}' .format('Not defined'))
		

	print '\n'
	print '\n3. CLUSTER configuration ...\n'
	print '-'*100

	clusterSet = []
	clusterDict = []
	machineSet = []
	hostDict = []
	serverDict = []
	serverTypeDict = {}
	sDict = {}
	deployDict = {}
	jdbcDict = []
	
	for cluster in root.findall('{http://xmlns.oracle.com/weblogic/domain}cluster'):
		clustername = cluster.find('{http://xmlns.oracle.com/weblogic/domain}name').text
		clusteraddress = cluster.find('{http://xmlns.oracle.com/weblogic/domain}cluster-address').text
		clustermessagingmode = cluster.find('{http://xmlns.oracle.com/weblogic/domain}cluster-messaging-mode').text
		clusterSet.append(clustername)
		clusterDict.append((clustername, 'cluster-address', clusteraddress))
		clusterDict.append((clustername, 'cluster-messaging-mode', clustermessagingmode))
		
	for currCluster in clusterSet:
		print '\n###### CLUSTER: ', currCluster, '######'

		print ('\n\t{0:45}\t\t{1:35}' .format('Parameter', 'Value'))
		print '\t', '='*45, '\t\t', '='*35 
		for clustername, clusterparameter, clusterparametervalue in clusterDict:
			if currCluster == clustername:
				print ('\t{0:45}\t\t{1:35}' .format(clusterparameter, clusterparametervalue))
	
	for hosts in root.findall('{http://xmlns.oracle.com/weblogic/domain}machine'):
		host = hosts.find('{http://xmlns.oracle.com/weblogic/domain}name').text
		machineSet.append(host)

	print '\n'
	print '\n4. SERVERS configuration ...\n'
	print '-'*100
	
	i = 0
	for server in root.findall('{http://xmlns.oracle.com/weblogic/domain}server'):
		servername = server.find('{http://xmlns.oracle.com/weblogic/domain}name').text
		listenaddress = server.find('{http://xmlns.oracle.com/weblogic/domain}listen-address').text
		serverDict.append((servername, 'listen-address', listenaddress))
		
		if servername != adminservername:
			listenport = server.find('{http://xmlns.oracle.com/weblogic/domain}listen-port').text
			serverDict.append((servername, 'listen-port', listenport))
			i=i+1
			sDict[i] = {}
			sDict[i].update({'server':servername, 'listen-address':listenaddress, 'listen-port':listenport, 'ssl':0})
			machine = server.find('{http://xmlns.oracle.com/weblogic/domain}machine').text
			hostDict.append((machine,servername))

			if server.find('{http://xmlns.oracle.com/weblogic/domain}ssl') is not None:
				for serverSSL in server.findall('{http://xmlns.oracle.com/weblogic/domain}ssl'):
					if serverSSL.find('{http://xmlns.oracle.com/weblogic/domain}enabled').text:
						lstport = serverSSL.find('{http://xmlns.oracle.com/weblogic/domain}listen-port').text
						i=i+1
						sDict[i] = {}
						sDict[i].update({'server':servername, 'listen-address':listenaddress, 'listen-port':lstport, 'ssl':1})
						
			for serverstart in server.findall('{http://xmlns.oracle.com/weblogic/domain}server-start'):
				arguments = serverstart.find('{http://xmlns.oracle.com/weblogic/domain}arguments').text

				if '-DwalledGarden=true' in arguments:
					serverTypeDict[servername] = 'BS'
				else:
					serverTypeDict[servername] = 'PS'					

			
			for networkaccesspoint in server.findall('{http://xmlns.oracle.com/weblogic/domain}network-access-point'):
				listenaddress = networkaccesspoint.find('{http://xmlns.oracle.com/weblogic/domain}listen-address').text
				listenport = networkaccesspoint.find('{http://xmlns.oracle.com/weblogic/domain}listen-port').text
				serverDict.append((servername, 'listen-address', listenaddress))
				serverDict.append((servername, 'listen-port', listenport))
				i=i+1
				sDict[i] = {}
				sDict[i].update({'server':servername, 'listen-address':listenaddress, 'listen-port':listenport, 'ssl':0})

	
	for app_deployments in root.findall('{http://xmlns.oracle.com/weblogic/domain}app-deployment'):
		deployment = app_deployments.find('{http://xmlns.oracle.com/weblogic/domain}name').text
		deploy_targets = app_deployments.find('{http://xmlns.oracle.com/weblogic/domain}target').text
		deployDict[deployment] = deploy_targets
		
	
	for host1 in machineSet:
	
		# BOOTSTRAP SERVERS
		print '\n###### HOST: ', host1, '######'
		print '\n=== BS Servers:'
		for host2, srv2 in hostDict:
			if host1 == host2:
				for srv, serverType in serverTypeDict.iteritems():
					if srv == srv2 and serverType == 'BS':
						print '\n-', srv
						print ('\n\t{0:30}\t\t{1:35}\t\t{2:30}' .format('Listen address', 'Listen port', 'Status'))
						print '\t', '='*30, '\t\t', '='*35, '\t\t', '='*30 
						for key, value in sDict.items():
							if sDict[key]['server'] == srv:
								try:
									socket.inet_aton(sDict[key]['listen-address'])
									host_ip = ''
								except:
									try:
										host_ip = socket.gethostbyname(sDict[key]['listen-address'])
									except:
										host_ip = 'unknown'
								
								if host_ip == '': 
									print ('\t{0:30}' .format(sDict[key]['listen-address'])),
								else:
									print ('\t{0:30}' .format(sDict[key]['listen-address'] + ' [' + host_ip + ']')),

								if sDict[key]['ssl']:
									print ('\t\t{0:35}' .format(sDict[key]['listen-port'] + ' [SSL]')),
									response = curl('https://'+sDict[key]['listen-address']+':'+ sDict[key]['listen-port']+'/hdm/')			# <<<<<<<<<<<<<<<<<<<<<<<<<<<<
								else:
									print ('\t\t{0:35}' .format(sDict[key]['listen-port'])),
									response = curl('http://'+sDict[key]['listen-address']+':'+ sDict[key]['listen-port']+'/hdm/')			# <<<<<<<<<<<<<<<<<<<<<<<<<<<<
									
								# import requests

								print '\t\tCURL: ', response.status


									
		# PUBLIC SERVERS
		print '\n=== PS Servers:'
		for host2, srv2 in hostDict:
			if host1 == host2:
				for srv, serverType in serverTypeDict.iteritems():
					if srv == srv2 and serverType == 'PS':
						print '\n-', srv
						print ('\n\t{0:30}\t\t{1:35}\t\t{2:30}' .format('Listen address', 'Listen port', 'Status'))
						print '\t', '='*30, '\t\t', '='*35, '\t\t', '='*30 
						for key, value in sDict.items():
							if sDict[key]['server'] == srv:
								try:
									socket.inet_aton(sDict[key]['listen-address'])
									host_ip = ''
								except:
									try:
										host_ip = socket.gethostbyname(sDict[key]['listen-address'])
									except:
										host_ip = 'unknown'
								
								if host_ip == '': 
									print ('\t{0:30}' .format(sDict[key]['listen-address'])),
								else:
									print ('\t{0:30}' .format(sDict[key]['listen-address'] + ' [' + host_ip + ']')),
									
								if sDict[key]['ssl']:
									print ('\t\t{0:35}' .format(sDict[key]['listen-port'] + ' [SSL]')),
									response = curl('https://'+sDict[key]['listen-address']+':'+ sDict[key]['listen-port']+'/hdm/')			# <<<<<<<<<<<<<<<<<<<<<<<<<<<<
								else:
									print ('\t\t{0:35}' .format(sDict[key]['listen-port'])),
									response = curl('http://'+sDict[key]['listen-address']+':'+ sDict[key]['listen-port']+'/hdm/')			# <<<<<<<<<<<<<<<<<<<<<<<<<<<<
									
								# import requests

								print '\t\tCURL: ', response.status
		
	print '\n\n5. DEPLOYMENTS...\n'
	print '-'*100
	
	if not deployDict:
		print '\n- Deployments not found'
	else:
		print ('\n\t{0:30}\t\t{1:35}' .format('Deployment', 'Target(s)'))
		print '\t', '='*30, '\t\t', '='*35 
		for deploy, target in sorted(deployDict.items()):
			print ('\t{0:30}\t\t{1:35}' .format(deploy,target))
				
	
	
	for jdbc_system_resource in root.findall('{http://xmlns.oracle.com/weblogic/domain}jdbc-system-resource'):
		jdbc_name = jdbc_system_resource.find('{http://xmlns.oracle.com/weblogic/domain}name').text
		jdbc_target = jdbc_system_resource.find('{http://xmlns.oracle.com/weblogic/domain}target').text
		jdbcDict.append((jdbc_name, jdbc_target))
		

	print '\n'
	print '\n6. JDBC configuration ...\n'
	print '-'*100

	print ('\n\t{0:45}\t\t{1:35}' .format('Name', 'Target'))
	print '\t', '='*45, '\t\t', '='*35 
	for jdbcname, jdbctarget in jdbcDict:
		print ('\t{0:45}\t\t{1:35}' .format(jdbcname, jdbctarget))


	print '\n', '='*30

	

	configXML.close()
	


# Handling errors 
def errHandler(FaultCode):
	Error = {
		'1' : 'You are running the script on unsupported OS',
		'2' : 'You are running unsupported profile',
		'3' : 'data.ini file should be present when collecting the active configuration',
		'4' : 'Path ' + WLSconfigdirectory + ' does not exists!',
		'5' : 'config.xml file is not present on ' + WLSconfigdirectory
	}
	sys.exit(Error.get(FaultCode))



# Main part of the script
def main():
	checkInput()
	print '\nExecution of the script is finished\n'
	
if __name__ == '__main__':
	main()