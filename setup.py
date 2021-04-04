import dataset
import datetime
import taskManager
Sys_date = datetime.datetime.now()

if __name__ == "__main__":
	taskbook_db = dataset.connect('sqlite:///taskbook.db')  
	task_table = taskbook_db.get_table('task')
	date_table = taskbook_db.get_table('view')
	task_table.drop()
	date_table.drop()
	task_table = taskbook_db.create_table('task')
	date_table = taskbook_db.create_table('view')
	date_table.insert(
		{"savedDate": taskManager.getdate_tomorrow(taskManager.getdate_today())}
	)

	user_db = dataset.connect('sqlite:///user.db')
	user_table = user_db.get_table('user')
	user_table.drop()
	user_table = user_db.create_table('user')

	session_db = dataset.connect('sqlite:///session.db')
	session_table = session_db.get_table('session')
	session_table.drop()
	session_table = session_db.create_table('session')
	# taskManager.insert_Tasks("Do something useful", status=True, repeatNum=1, startDt="2021-2-21", col="blue")
	# taskManager.insert_Tasks("Do something fantastic", endDt='2021-2-21', col="green")
	# taskManager.insert_Tasks("Do something remarkable", endDt='2021-2-20', col="red")
	# taskManager.insert_Tasks("Do something unusual", status=True, endDt='2021-2-22', col="gray")
