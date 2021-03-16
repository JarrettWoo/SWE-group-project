import dataset
import datetime
import taskManager
Sys_date = datetime.datetime.now()

if __name__ == "__main__":
    taskbook_db = dataset.connect('sqlite:///taskbook.db')  
    task_table = taskbook_db.get_table('task')
    task_table.drop()
    task_table = taskbook_db.create_table('task')
    taskManager.insert_Tasks("Do something useful", status=True, repeatNum=1, startDt="2021-2-21", col="blue")
    taskManager.insert_Tasks("Do something fantastic", endDt='2021-2-21', col="green")
    taskManager.insert_Tasks("Do something remarkable", endDt='2021-2-20', col="red")
    taskManager.insert_Tasks("Do something unusual", status=True, endDt='2021-2-22', col="gray")