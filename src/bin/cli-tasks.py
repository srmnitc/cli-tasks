#!/usr/bin/python
"""
Command line task management system in python.

Main file which provides the command line interface
"""

import argparse as ap
from cli-tasks import create_task,output_tasks,reset,done,delete


def main():
	"""
	Main function which runs when cli-tasks is called
	"""
	arg = ap.ArgumentParser(description="cli-tasks command line taskbook\n. ",usage='''
			cli-tasks <command> [<args>]

			Short guide
			-----------
			task -d (--description) : description
			optional: -w (--when) : due date
				  -p (--priority) : 1(high),2(medium) or 3(low)
				  -g (--group) : name of the task group
			show (--fetch) [all, <groupname> ]
				   fetch all tasks or by group
			done (--done) <task number> : mark the task as done

		''')

	#add a subarg parser
	subarg = arg.add_subparsers(dest='main_option')

	#th main parser part for task
	arg_task = subarg.add_parser("new",help="keyword to add a task")
	#now sub args for this one
	#description
	arg_task.add_argument("-d", "--description", required=True,
	help="specify -d followed by task description")
	#due date
	arg_task.add_argument("-w", "--when", required=False,
	help="specify -w followed by task due date")
	#priority
	arg_task.add_argument("-p", "--priority", required=False, type=int, choices=[1,2,3],
	help="specify -p followed by priority of 1,2 or 3")
	#group
	arg_task.add_argument("-g", "--group", required=False,
	help="specify -g followed by groupname")


	#the show commands
	arg_task = subarg.add_parser("show",help="keyword to add a task")
	arg_task.add_argument("-g", "--group", required=False,
	help="specify -g followed by groupname")

	#the mark commands
	arg_task = subarg.add_parser("done",help="keyword to add a task")

	#the mark commands
	arg_task = subarg.add_parser("delete",help="keyword to add a task")

	#the reset command
	arg_task = subarg.add_parser("reset",help="reset the tasks file")


	taskdetails = vars(arg.parse_args())


	if taskdetails['main_option'] is 'new':
		create_task(taskdetails)
		print("task created")
	elif taskdetails['main_option'] is 'show':
		dontneed = output_tasks(taskdetails["group"])
	elif taskdetails['main_option'] is 'reset':
		reset()
	elif taskdetails['main_option'] is 'done':
		done()
	elif taskdetails['main_option'] is 'delete':
		delete()
