
# Import Functions
import dataset
import datetime
from datetime import timedelta
import time
from bottle import request

# Establishing Database connection
taskbook_db = dataset.connect('sqlite:///taskbook.db')
session_db = dataset.connect('sqlite:///session.db')
task_table = taskbook_db.get_table('task')
date_table = taskbook_db.create_table('view')


# Returns a formatted date string in the form Year-Month-Day
def getdate_today():
    Sys_date = datetime.datetime.now()
    return Sys_date.strftime("%Y-%m-%d")

def getdate_tomorrow(today):
    year, month, day = today.split('-')
    date = datetime.datetime(int(year), int(month), int(day))
    date = date + timedelta(days=1)
    return date.strftime("%Y-%m-%d")


# Getter and setter for the remembered day in view table
def get_view():
    date_list = [dict(x) for x in date_table.find()]
    return date_list[0]


def set_view(date):
    print("I have set the new day!")
    date_list = [dict(x) for x in date_table.find()][0]
    date_list['savedDate'] = date
    date_table.update(row=date_list, keys=['id'])



# A basic revision for the insertion of tasks into the tasks table. Will further revise to include functionality
# for inserting multiple lines of tasks.
def insert_Tasks(taskDef, status=False, dateList = '', repeatNum = 0, startDt = getdate_today(), endDt = ''):

    # Current Revised Data Structure:
    """
        time: Timestamp for when the task was written, needed for proper execution and organization of tasks
        description: Description of the task
        list: Legacy attribute needed to proper functionality. Will remove when no longer needed.
        completed: Boolean variable that dictates whether or not a task is crossed out on the list
        repeatFreq: An integer variable that dictates how often a task repeats:
            0 --> No repeat
            1 --> Daily repeat
            2 --> Repeat every 2 days
            ...
            7 --> Repeat weekly
            ...
        startDate: Determines when a task should start being included in the task list for a given date
        endDate: Determines the last possible day for a task to be included on a task list

    """
    task_table.insert(
        {"time":time.time(), "user":getUser(), "description":taskDef, "list":dateList, "completed":status,
         "repeatFreq":repeatNum, "startDate":startDt, "endDate":endDt, "color":col}
    )


# Returns a dictionary with a single element to the requesting function:
# Key being the word "tasks" and the value is a list of all tasks being returned
def get_tasks(dates):

    # Pulls every task out of the database into a working list
#    tasks_list = [dict(x) for x in task_table.find()]

    # Pulls tasks associated with 'user' into a working list
    tasks_list = [dict(x) for x in task_table.find(user = getUser())]

    # This is the list tasks will be inserted into to be returned
    tasks = []

    for d in dates:
        year, month, day = d.split('-')
        viewDay = datetime.datetime(int(year), int(month), int(day))

        for task in tasks_list:
            viewTask = dict(task)
            stYear, stMonth, stDay = viewTask['startDate'].split('-')
            startDay = datetime.datetime(int(stYear), int(stMonth), int(stDay))

            # A task cannot be returned if it has not yet started
            if startDay <= viewDay:
                if viewTask['endDate'] == '':

                    # If a task has a repeatFreq of 0, this if statement avoids a divide by zero error
                    if viewTask['repeatFreq'] == 0:
                        if startDay == viewDay:
                            viewTask['list'] = viewDay.strftime("%Y-%m-%d")
                            viewTask['id'] = viewDay.strftime("%Y-%m-%d") + '-' + str(viewTask['id'])
                            tasks.append(viewTask)
                    else:
                        # A task is passed into the list if the number of days between the current date
                        # and the start date is a multiple of the frequency of the task
                        numDays = int((viewDay - startDay).days)
                        if numDays % viewTask['repeatFreq'] == 0:
                            viewTask['list'] = viewDay.strftime("%Y-%m-%d")
                            viewTask['id'] = viewDay.strftime("%Y-%m-%d") + '-' + str(viewTask['id'])
                            tasks.append(viewTask)

                else:
                    endYear, endMonth, endDay = viewTask['endDate'].split('-')
                    endDay = datetime.datetime(int(endYear), int(endMonth), int(endDay))

                    # A task cannot be returned if it has ended
                    if viewDay <= endDay:

                        # Same logic as described above
                        if viewTask['repeatFreq'] == 0:
                            if startDay == viewDay:
                                viewTask['list'] = viewDay.strftime("%Y-%m-%d")
                                viewTask['id'] = viewDay.strftime("%Y-%m-%d") + '-' + str(viewTask['id'])
                                tasks.append(viewTask)
                        else:
                            numDays = int((viewDay - startDay).days)
                            if numDays % viewTask['repeatFreq'] == 0:
                                viewTask['list'] = viewDay.strftime("%Y-%m-%d")
                                viewTask['id'] = viewDay.strftime("%Y-%m-%d") + '-' + str(viewTask['id'])
                                tasks.append(viewTask)

    return { "tasks": tasks }
