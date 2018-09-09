import json
from task_container import task
from clint.textui import puts, colored
from clint.textui import columns

def create_task(taskdetails):
	with open("tasks.json","a") as write_file:
		json.dump(taskdetails,write_file)
		write_file.write("\n")

def fetch_task():
	data = []
	with open("tasks.json","r") as read_file:
		for line in read_file:
			data.append(json.loads(line))
	return data

def output_tasks(data):
	col=50
	colsmall = 10
	puts(columns([(colored.blue('--------------------------------------------------')), col], [(colored.blue('----------')), colsmall]))
	puts(columns([(colored.blue('Task')), col], [(colored.blue('When?')), colsmall]))
	puts(columns([(colored.blue('--------------------------------------------------')), col], [(colored.blue('----------')), colsmall]))
	for d in data:
		if d["when"]==None:
			d["when"]="whenever"
		puts(columns([d["task"], col], [d["when"].strip(), colsmall]))
	puts(columns([(colored.blue('--------------------------------------------------')), col], [(colored.blue('----------')), colsmall]))