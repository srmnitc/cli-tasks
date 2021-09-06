#!/usr/bin/python
"""
Command line task management system in python.

Main file which provides the command line interface
"""

import argparse as ap
from clitasks.tasks import Task


def main():
	"""
	Main function which runs when cli-tasks is called
	"""
	arg = ap.ArgumentParser(description="cli-tasks command line taskbook\n. ",usage='''
			todo <command> [<args>]

			Short guide
			-----------
			add:
				-t (--title) : title of task
				-d (--description) : description of task
				-w (--when) : due date
				-p (--priority) : 1(high),2(medium) or 3(low)
				-g (--group) : name of the task group
			
			show: 
				-f (--fetch) : fetch all tasks or by group

			done: 
				-d (--done) <task number> : mark the task as done
			
			remove: remove all tasks

		''')

	#add a subarg parser
	subarg = arg.add_subparsers(dest='main_option')

	#th main parser part for task
	add_task = subarg.add_parser("add",help="keyword to add a task")

	#title
	add_task.add_argument("-t", "--title", required=True,
	help="specify -t followed by task title")	
	#description
	add_task.add_argument("-d", "--description", required=False,
	help="specify -d followed by task description")
	#due date
	add_task.add_argument("-w", "--when", required=False,
	help="specify -w followed by task due date")
	#priority
	add_task.add_argument("-p", "--priority", required=False, 
		type=int, choices=[1,2,3],
	help="specify -p followed by priority of 1,2 or 3")
	#group
	add_task.add_argument("-g", "--group", required=False,
	help="specify -g followed by groupname")


	#the show commands
	show_task = subarg.add_parser("show",help="keyword to show tasks")
	show_task.add_argument("-g", "--group", required=False,
	help="specify -g followed by groupname")

	#the mark commands
	done_task = subarg.add_parser("done",help="keyword to mark a task as done")

	#the mark commands
	remove_task = subarg.add_parser("remove",help="keyword to remove all tasks")


	taskdetails = vars(arg.parse_args())

	task = Task()

	if taskdetails['main_option'] == 'add':
		task.create_task(taskdetails)
		print("task created")
	
	elif taskdetails['main_option'] == 'show':
		_ = task.output_tasks(group=taskdetails["group"])
	
	elif taskdetails['main_option'] == 'done':
		task.done(group=taskdetails["group"])
	
	elif taskdetails['main_option'] == 'remove':
		task.done()
	
	elif taskdetails['main_option'] == 'delete':
		task.delete(group=taskdetails["group"])
	
	else:
		print(taskdetails['main_option'])
		print("Unknown main option")
