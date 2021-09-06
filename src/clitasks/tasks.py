import os
import datetime
import sys
import random
from tinydb import TinyDB, Query
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.prompt import IntPrompt
import uuid

from clitasks.task_container import task
from clitasks.quote import quotes

#some things that re needed
StrptimeFmt = "%Y-%m-%d %H:%M:%S.%f"

class Task:
    """
    Class to hold all task details
    """
    def __init__(self):
        """
        Do an init run
        """
        #set up a task dict
        self.taskdir = os.path.join(os.environ['HOME'],
            'cli-tasks')
        self.taskfile = os.path.join(self.taskdir, 
            'tasks.json')
        self.taskbackup = ".".join([self.taskfile, 
            'bkup'])
        if not os.path.exists(self.taskdir):
            print("task dir not found, creating one..")
            os.mkdir(self.taskdir)
        #start a db connection
        self.db = db = TinyDB(self.taskfile)

    def write_task(self, taskdetails):
        """
        Write a task to db
        """
        self.db.insert(taskdetails)

    def create_task(self, taskdetails):
        """
        Create a new task
        """
        #remove the main_option
        taskdetails.pop('main_option', None)
        
        #we have to add the current date as the date of setting the task
        now = datetime.datetime.now()
        
        #add the time to the dictionary
        taskdetails["created"] = now.__str__()
        taskdetails["status"] = False
        taskdetails["id"] = str(uuid.uuid4())

        self.write_task(taskdetails)

    def fetch_task(self):
        """
        Fetch all tasks
        """
        data = self.db.all()
        return data

    def output_tasks(self, group = None):
        """
        Fetch tasks by group
        """
        if group is not None:
            Group = Query()
            data = self.db.search(Group.group == group)
        else:
            data = self.fetch_task()
        self.formatted_print(data)
        return data

    def color_text(self, strtocolor, priority):
        """
        Color text according to priority
        """
        prdict = {"1": "#EF5350", "2": "#FF8F00", "3": "#9E9D24", "0": "#78909C", "9":"#42A5F5"}
        text = Text()
        text.append(str(strtocolor), style=prdict[str(priority)])
        return text

    def get_done_tasks(self, data):
        """
        Get percentage of tasks done
        """
        datadone = []
        datanotdone = []

        for d in data:
            if d["status"]:
                datadone.append(d)
            else:
                datanotdone.append(d)

        return datadone, datanotdone

    def formatted_print(self, data):
        """
        Print formatted data
        """
        datadone, datanotdone = self.get_done_tasks(data)
        donepercent = "%d"%((len(datadone)//len(datanotdone))*100)

        table = Table(title="cli tasks", style="white")
        table.add_column("#")
        table.add_column("Time")
        table.add_column("Status")
        table.add_column("Title")
        table.add_column("Details")
        table.add_column("Priority")
        table.add_column("Due")
        table.add_column("Group")
        
        for count, d in enumerate([*datanotdone, *datadone]):
            
            time, timestr = self.find_from_when(d)
            if d["status"]:
                r2 = ":heavy_check_mark:"
                d['priority'] = 0
                r0 = self.color_text("-", d['priority'])
            else:
                r2 = ":x:"
                r0 = self.color_text("%s"%str(count+1), d['priority'])
                

            r1 = "%.1f %s ago.."%(time, timestr)
            r1 = self.color_text(r1, d['priority'])        
            r3 = self.color_text(d["title"], d['priority'])
            r4 = self.color_text(d['description'], d['priority'])
            r5 = self.color_text(d['priority'], d['priority'])
            r6 = self.color_text(d['due'], d['priority'])
            r7 = self.color_text(d['group'], d['priority'])
            table.add_row(r0, r1, r2, r3, r4, r5, r6, r7)

        console = Console()
        console.print(table)
        t = self.color_text("%s%% tasks done!"%donepercent, 0)
        console.print(t)
        t = self.color_text(self.random_quote(), 9)
        console.print(t)

    def delete(self, group=None):
        """
        Delete tasks
        """
        if group == "all":
            self.reset()
        else:
            data = self.output_tasks(group=group)
            datadone, datanotdone = self.get_done_tasks(data)

            if len(datanotdone) == 0:
                print("nothing to delete!")
                return

            #now ask for option
            dno = IntPrompt.ask("Which task should be deleted? (1-%d)"%len(datanotdone))
            if not (0 < dno <= len(datanotdone)):
                print("choose a valid option")
                return

            dkey = datanotdone[dno]["id"]
            Group = Query()
            self.db.remove(Group.id == dkey)
            print('deleted')

    def done(self, group=None):
        """
        Mark tasks as done
        """
        data = self.output_tasks(group=group)
        datadone, datanotdone = self.get_done_tasks(data)

        if len(datanotdone) == 0:
            print("nothing to mark as done!")
            return

        #now ask for option
        dno = IntPrompt.ask("Which task should be marked as done? (1-%d)"%len(datanotdone))
        if not (0 < dno <= len(datanotdone)):
            print("choose a valid option")
            return

        dkey = datanotdone[dno]["id"]
        Group = Query()
        self.db.update({'status': True}, Group.id == dkey)
        print('updated')


    def random_quote(self):
        i = random.randint(0,len(quotes)-1)
        return quotes[i]

    def reset(self):
        """
        Hard reset all tasks
        """
        dno = IntPrompt.ask("This will really delete all tasks, press 1 to continue.")        
        if dno==1:
            self.db.truncate()

    def find_from_when(self, d):
        """
        Find from when task is pending
        """
        created = datetime.datetime.strptime(d["created"],StrptimeFmt)
        if d["status"]==True:
            created = datetime.datetime.strptime(d["finished"],StrptimeFmt)
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


