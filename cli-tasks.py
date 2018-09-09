#!/usr/bin/python

import argparse as ap
from src import create_task,fetch_task,output_tasks
#arg = ap.ArgumentParser()
#argument mode
arg = ap.ArgumentParser(description="cli-tasks command line taskbook\n. ",usage='''
		cli-tasks <command> [<args>]

		cli-tasks take two arguments
		add - adds a task to list and can be accompanied by options
		-t (--task) <title>
		fetch - shows tasks

	''')

#add a subarg parser
subarg = arg.add_subparsers()

arg_add = subarg.add_parser("add",help="keyword to add a note or task")
#add a note with title
arg_add.add_argument("-t", "--task", required=True,
help="specify -t followed by task title")
#description
arg_add.add_argument("-d", "--description", required=False,
help="specify -d followed by task description")
#due
arg_add.add_argument("-w", "--when", required=False,
help="specify -w followed by task due date")

arg_fetch = subarg.add_parser("fetch",help="keyword to fetch a note or task")

arg_fetch.add_argument("-i", "--item", required=True, choices=['task'],
help="specify -i followed by task")

taskdetails = vars(arg.parse_args())


if "task" in taskdetails.keys():
	create_task(taskdetails)
	print "task created"
elif "item" in taskdetails.keys():
	if taskdetails["item"]=="task":
		tdata = fetch_task()
		output_tasks(tdata)
		print "finished"
