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

	print "Which operation do you want to run?"
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
	while ( pre_post_num != 1 ) and ( pre_post_num != 2 ):
		pre_post_num = int( raw_input("Is this a [1] pre-event or [2] post-event snapshot?\n[1|2]: "))

	while ( device == "<none>" ) or ( device == "" ):
		device = raw_input("Device to snapshot: ")

	while (ip_name == "<none>" ) or ( ip_name == "" ):
		ip_name = raw_input("IP or DNS name of device: " )

	while (cfg_file == "<none>" ) or ( cfg_file == "" ):
		cfg_file = raw_input("SNAP config file to use: " )

	#while (location == "<none>" ) or ( location == "" ):
		#location = raw_input("Destination for results: " )

	while (username == "<none>" ) or ( username == "" ):
		username = raw_input("Username: " )

	while (password == "<none>" ) or ( password == "" ):
		password = getpass.getpass("Password: " )

	# Now lets concatenate the args into one string
	args = str( "--snap " + device + "-" + pre_post[ pre_post_num ] + " -l " + username + " -p " + password + " -t " + ip_name + " " + cfg_file )

	return args

def get_check_args():
	"""
	Interactively grab some real data from the user and build the
	argument string we will need to run a jsnap check.  Return
	the argument string.
	"""

def get_snapcheck_args():
	"""
	Interactively grab some real data from the user and build the
	argument string we will need to run a jsnap snapcheck.  Return
	the argument string.
	"""


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
