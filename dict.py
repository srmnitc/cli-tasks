
from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
import json
import os
import sys
from clint.arguments import Args
from clint.textui import puts, colored, indent

#process the args
args = Args()

#here we switch between interactive or command line mode
#terminal mode - 0, interactive - 1
vmode=0
kmode=''

#now process the flags
argflags = dict(args.grouped)
#print(argflags)
#process the arguments
#at this point, mode, firstname and surname
#lets simplify modes
kmodelist = ['-mode','-m']
vmodelist = ['interactive','i']


#now lets assign the value
if '-m' in args.flags:
	try: 
		if argflags["-mode"].all[0] in vmodelist
			puts(colored.red("interactive2"))
			break
	try: 
		argflags["-m"].all[0] in vmodelist:
		puts(colored.green("interactive2"))
		break
	except:
		puts(colored.blue("interactive2"))

identity = [
    {
        'type': 'input',
        'name': 'first_name',
        'message': 'What\'s your first name',
    },
    
    {
        'type': 'input',
        'name': 'surname',
        'message': 'What\'s your surname',
    }
]

#some questions for the identity
#first read in json-first task
infofound = False
if os.path.exists("test.json"):
	with open("test.json", "r") as read_file:
		data = json.load(read_file)
    	if data["first_name"]!='':
    		infofound=True

if not infofound:
	print("nothing")