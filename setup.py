import dataset
import datetime
import taskManager
Sys_date = datetime.datetime.now()

if __name__ == "__main__":
    taskbook_db = dataset.connect('sqlite:///taskbook.db')  
    task_table = taskbook_db.get_table('task')
    task_table.drop()
    task_table = taskbook_db.create_table('task')
    taskManager.insert_Tasks("Do something useful", status=True, endDt="2022-3-18")
    taskManager.insert_Tasks("Do something fantastic", endDt='2021-2-21')
    taskManager.insert_Tasks("Do something remarkable", endDt='2021-2-20')
    taskManager.insert_Tasks("Do something unusual", status=True, endDt='2021-2-22')

    tasks = [dict(x) for x in task_table.find(order_by='time')]
    print(len(tasks))
    for task in tasks:
        print(task)