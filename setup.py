import dataset
import datetime
import taskManager
Sys_date = datetime.datetime.now()

if __name__ == "__main__":
    taskbook_db = dataset.connect('sqlite:///taskbook.db')  
    task_table = taskbook_db.get_table('task')
    date_table = taskbook_db.create_table('view')
    task_table.drop()
    date_table.drop()

    task_table = taskbook_db.create_table('task')
    date_table = taskbook_db.create_table('view')

    date_table.insert(
        {"savedDate": taskManager.getdate_tomorrow(taskManager.getdate_today())}
    )

    taskManager.insert_Tasks("Do something useful", status=True, repeatNum=1, startDt='2021-3-25')
    taskManager.insert_Tasks("Do something fantastic", endDt='2021-3-27')
    taskManager.insert_Tasks("Do something remarkable", endDt='2021-2-20')
    taskManager.insert_Tasks("Do something unusual", status=True, endDt='2021-3-25')
