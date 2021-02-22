import dataset
import datetime
import time

taskbook_db = dataset.connect('sqlite:///taskbook.db')
task_table = taskbook_db.get_table('task')


def getdate_today():
    Sys_date = datetime.datetime.now()
    return Sys_date.strftime("%Y-%m-%d")


def insert_Tasks(taskDef, status=False, dateList = 'today', repeatNum = 0, startDt = getdate_today(), endDt = ''):

    task_table.insert(
        {"time":time.time(), "description":taskDef, "list":dateList, "completed":status,
         "repeatFreq":repeatNum, "startDate":startDt, "endDate":endDt}
    )


def get_tasks(date):
    tasks_list = [dict(x) for x in task_table.find()]
    tasks = []

    year, month, day = date.split('-')
    viewDay = datetime.datetime(int(year), int(month), int(day))

    for task in tasks:
        print(task)
    for task in tasks_list:
        stYear, stMonth, stDay = task['startDate'].split('-')
        startDay = datetime.datetime(int(stYear), int(stMonth), int(stDay))

        if startDay <= viewDay:
            print(task['endDate'])
            if task['endDate'] == '':
                if task['repeatFreq'] == 0:
                    tasks.append(task)
                else:
                    numDays = int((viewDay - startDay).days)
                    if numDays % task['repeatFreq'] == 0:
                        tasks.append(task)

            else:
                endYear, endMonth, endDay = task['endDate'].split('-')
                endDay = datetime.datetime(int(endYear), int(endMonth), int(endDay))

                if viewDay <= endDay:
                    if task['repeatFreq'] == 0:
                        tasks.append(task)
                    else:
                        numDays = int((viewDay - startDay).days)
                        if numDays % task['repeatFreq'] == 0:
                            tasks.append(task)

    print({"tasks": tasks})
    return { "tasks": tasks }
