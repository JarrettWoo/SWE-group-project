
# Import Functions
import dataset
import datetime
import time

# Establishing Database connection
taskbook_db = dataset.connect('sqlite:///taskbook.db')
task_table = taskbook_db.get_table('task')


# Returns a formatted date string in the form Year-Month-Day
def getdate_today():
    Sys_date = datetime.datetime.now()
    return Sys_date.strftime("%Y-%m-%d")


# A basic revision for the insertion of tasks into the tasks table. Will further revise to include functionality
# for inserting multiple lines of tasks.
def insert_Tasks(taskDef, status=False, dateList = 'today', repeatNum = 0, startDt = getdate_today(), endDt = ''):

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
        {"time":time.time(), "description":taskDef, "list":dateList, "completed":status,
         "repeatFreq":repeatNum, "startDate":startDt, "endDate":endDt}
    )


# Returns a dictionary with a single element to the requesting function:
# Key being the word "tasks" and the value is a list of all tasks being returned
def get_tasks(date):

    # Pulls every task out of the database into a working list
    tasks_list = [dict(x) for x in task_table.find()]

    # This is the list tasks will be inserted into to be returned
    tasks = []

    year, month, day = date.split('-')
    viewDay = datetime.datetime(int(year), int(month), int(day))

    for task in tasks_list:
        stYear, stMonth, stDay = task['startDate'].split('-')
        startDay = datetime.datetime(int(stYear), int(stMonth), int(stDay))

        # A task cannot be returned if it has not yet started
        if startDay <= viewDay:
            if task['endDate'] == '':

                # If a task has a repeatFreq of 0, this if statement avoids a divide by zero error
                if task['repeatFreq'] == 0 and startDay == viewDay:
                    tasks.append(task)
                else:
                    # A task is passed into the list if the number of days between the current date
                    # and the start date is a multiple of the frequency of the task
                    numDays = int((viewDay - startDay).days)
                    if numDays % task['repeatFreq'] == 0:
                        tasks.append(task)

            else:
                endYear, endMonth, endDay = task['endDate'].split('-')
                endDay = datetime.datetime(int(endYear), int(endMonth), int(endDay))

                # A task cannot be returned if it has ended
                if viewDay <= endDay:

                    # Same logic as described above
                    if task['repeatFreq'] == 0 and startDay == viewDay:
                        tasks.append(task)
                    else:
                        numDays = int((viewDay - startDay).days)
                        if numDays % task['repeatFreq'] == 0:
                            tasks.append(task)

    return { "tasks": tasks }
