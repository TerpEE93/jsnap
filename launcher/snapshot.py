#!/usr/bin/python
#
# snapshot
#
#    A simple script to prompt for variables and then run jsnap
#    with the variables supplied by the user.  At least it will
#    hide the password from full display :-)
#
#    I put this in /usr/local/bin on my system.  Feel free to
#    put it wherever works best for you.
#

import getpass
import subprocess

# Setup some defaults
jsnap_cmd = "/usr/jawa/bin/jsnap"
cfg_folder = "/usr/local/lib/jsnap"
jsnap_args = "<none>"
operation = "0"

def get_operation():
	"""
	Determine which jsnap operation the user wants.  Choices are:
	1. snap: Snapshot data and save as collection 'name'
	2. check: Check results of two snapshot collections 'name1' and 'name2'
	3. snapcheck: Take a single snapshot as collection 'name' and checks results

	This drives the rest of the process
	"""

	op = "0"

	print "\nWhich operation do you want to run?"
	print "1. snap: Snapshot data and save as collection 'name'"
	print "2. check: Check results of two snapshot collections 'name1' and 'name2'"
	print "3. snapcheck: Take a single snapshot as collection 'name' and checks results"

	while ( op < "1" ) or (op > "3" ):
		op = raw_input("[1-3]: ")

	return op

def get_snap_args():
	"""
	Interactively grab some real data from the user and build the
	argument string we will need to run a jsnap snapshot.  Return
	the argument string.
	"""

	# Local variables
	args = "<none>"
	pre_post_num = 0
	pre_post = [ "<none>", "pre", "post" ]
	device = "<none>"
	ip_name = "<none>"
	cfg_file = "<none>"
	location = "<none>"
	username = "<none>"
	password = "<none>"

	# Get real data from the user
	pre_post_num = get_pre_post()
	device = get_device()
	ip_name = get_ip_name()
	cfg_file = get_config_file( )
	username = get_username()
	password = get_password()

	#while (location == "<none>" ) or ( location == "" ):
		#location = raw_input("Destination for results: " )

	# Now lets concatenate the args into one string
	args = str( "--snap " + device + "-" + pre_post[ pre_post_num ] + " -l " + username + " -p " + password + " -t " + ip_name + " " + cfg_file )
	return args

def get_check_args():
	"""
	Interactively grab some real data from the user and build the
	argument string we will need to run a jsnap check.  Return
	the argument string.
	"""

	device = "<none>"
	ip_name = "<none>"
	cfg_file = "<none>"

	device = get_device()
	ip_name = get_ip_name()
	cfg_file = get_config_file()

	args = str( " --check " + device + "-pre," + device + "-post " + " -t " + ip_name + " " + cfg_file )
	return args

def get_snapcheck_args():
	"""
	Interactively grab some real data from the user and build the
	argument string we will need to run a jsnap snapcheck.  Return
	the argument string.
	"""

	args = "<none>"
	device = "<none>"
	ip_name = "<none>"
	cfg_file = "<none>"
	location = "<none>"
	username = "<none>"
	password = "<none>"

	device = get_device()
	ip_name = get_ip_name()
	cfg_file = get_config_file()
	username = get_username()
	password = get_password()

	#while (location == "<none>" ) or ( location == "" ):
		#location = raw_input("Destination for results: " )

	# Now lets concatenate the args into one string
	args = str( "--snapcheck " + device + " -l " + username + " -p " + password + " -t " + ip_name + " " + cfg_file )
	return args

def get_pre_post():
	"""
	Ask user if this is a pre-event snapshot or a post-event snapshot
	"""

	x = 0

	while ( x != 1 ) and ( x != 2 ):
		x = int( raw_input("\nIs this a [1] pre-event or [2] post-event snapshot?\n[1|2]: "))

	return x

def get_device():
	"""
	Ask user which device (by name) we are snapshotting
	"""

	device = "<none>"

	while ( device == "<none>" ) or ( device == "" ):
		device = raw_input("\nDevice to snapshot: ")

	return device

def get_ip_name():
	"""
	Prompt user for IP or hostname
	"""

	ip_name = "<none>"

	while (ip_name == "<none>" ) or ( ip_name == "" ):
		ip_name = raw_input("\nIP or DNS name of device: " )

	return ip_name

def get_config_file():
	"""
	What jsnap config file should we use?
	"""

	full_file_name = "<none>"
	cfg_file_ref = -1
	i=0

	file_names = list_folder()

	for file in file_names:
		print i, "    ", file
		i += i

	while (cfg_file_ref < 0 ) or ( cfg_file_ref > i ):
		cfg_file_ref = int( raw_input("\nSNAP config file to use: " ) )

	full_file_name = cfg_folder + "/" + file_names[cfg_file_ref]

	return full_file_name

def get_username():
	"""
	Ask user to supply a username
	"""

	username = "<none>"

	while (username == "<none>" ) or ( username == "" ):
		username = raw_input("\nUsername: " )

	return username

def get_password():
	"""
	Ask user for a valid password
	Note the password will not be echoed
	"""

	password = "<none>"

	while (password == "<none>" ) or ( password == "" ):
		password = getpass.getpass("\nPassword: " )

	return password

def list_folder():
   """
   Dump the contents of a folder (directory)
   Returns data as a list
   """

   proc = subprocess.Popen( ['ls', cfg_folder], stdout = subprocess.PIPE )
   output = proc.stdout.read()
   file_list = output.split( '\n' )[:-1]

   return file_list





operation = get_operation()

if operation == "1":
	jsnap_args = get_snap_args()
elif operation == "2":
	jsnap_args = get_check_args()
elif operation == "3":
	jsnap_args = get_snapcheck_args()
else:
	print "That was weird.  Seems you didn't choose a valid operation."
	exit( 1 )

print "args are:", jsnap_args

subprocess.call([jsnap_cmd, jsnap_args])
