import json
import os
from task_container import task
from clint.textui import puts, colored
from clint.textui import columns
import datetime

#some things that re needed
StrptimeFmt = "%Y-%m-%d %H:%M:%S.%f"
#done = colored.green("0")
#notdone = colored.red("0")


def create_task(taskdetails):
	#remove the main_option
	taskdetails.pop('main_option', None)
	#we have to add the current date as the date of setting the task
	now = datetime.datetime.now()
	#add the time to the dictionary
	taskdetails["created"] = now.__str__()
	taskdetails["status"] = False
	#print taskdetails["created"]
	#try to reconvert
	write_task(taskdetails)

def fetch_task():
	data = []
	with open("tasks.json","r") as read_file:
		for line in read_file:
			data.append(json.loads(line))
	return data

def output_tasks(group=None):
	#first sort by groups
	data = fetch_task()
	if group!=None:
		data = [d for d in data if d["group"]==group ]
	formatted_print(data)


def formatted_print(data):


	#we need autoformating
	colsize = find_colsize(data)
	col = colsize+5
	col2 = 50
	colsupersmall = 1

	#do header
	totcol = col+col2+colsupersmall
	header(totcol)

	count=0
	finished=0
	for d in data:
		count+=1
		#fix the time
		d = fix_when(d)
		#find when the task was added
		ttime,tstring = find_from_when(d)
		#format the color according to priority
		taskname = color_priority(d)
		#now we are ready to print out
		taskstring = ((" added %d %s ago, due %s, @%s")%(ttime,tstring,d["when"],d["group"]))
		taskstring = colored.white(taskstring)
		
		#get the status
		if d["status"]==True:
			status = colored.green("0")
			finished+=1
		else:
			status = colored.red("0")

		puts(columns([(str(count)), colsupersmall],[(status), colsupersmall],[(taskname), col], [(taskstring), col2]))
		#puts('{0: <80}'.format(taskname)+ taskstring)
	finished = finished/float(count)
	footer(totcol)
	print " %2.2f %% tasks done!"%finished
	footer(totcol)

def delete():
	data = fetch_task()
	formatted_print(data)
	doneid = input("Serial number of task to be deleted: ")
	data.pop(doneid-1)
	reset()
	for d in data:
		write_task(d)
	print "deleted!"

def done():
	data = fetch_task()
	formatted_print(data)
	doneid = input("Serial number of task to be marked done: ")
	data[doneid-1]["status"]=True
	reset()
	for d in data:
		write_task(d)
	print "done!"



def reset():
	if os.path.exists("#tasks.json#"):
		os.remove("#tasks.json#")
	os.rename("tasks.json","#tasks.json#")

#some random helpers
def header(col):
	puts(columns([(colored.blue('-'*col)), col]))
	print "Tasks"
	#puts(columns([(colored.white('Tasks')), col]))
	puts(columns([(colored.blue('-'*col)), col]))

def footer(col):
	puts(columns([(colored.blue('-'*col)), col]))


def fix_when(d):
	if d["when"]==None:
		d["when"]="whenever"
	return d

def find_from_when(d):
	created = datetime.datetime.strptime(d["created"],StrptimeFmt)
	now = datetime.datetime.now()
	diff = now-created
	days = diff.days
	tstring = "days"
	ttime = days
	if days==1:
		tstring = "day"
	elif days<=0:
		hours = diff.seconds/3600
		tstring = "hours"
		ttime = hours
		if hours==1:
			tstring = "hour"
		elif hours<1:
			ttime = diff.seconds/60
			tstring = "minutes"
			if ttime<=1:
				tstring = "minute"
		elif hours<=0:
			tstring = "seconds"
			ttime = diff.seconds
			if ttime==1:
				tsrting="second"

	return ttime,tstring

def color_priority(d):
	if d["priority"]==None:
		return colored.white(d["description"])
	elif d["priority"]==1:
		return colored.red(d["description"])
	if d["priority"]==2:
		return colored.yellow(d["description"])
	if d["priority"]==3:
		return colored.green(d["description"])



def find_colsize(data):

	maxlength = 0
	lens = [len(x["description"]) for x in data ]
	return max(lens)		

def write_task(taskdetails):
	with open("tasks.json","a") as write_file:
		json.dump(taskdetails,write_file)
		write_file.write("\n")
	write_file.close()