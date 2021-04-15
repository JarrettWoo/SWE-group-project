# SWIFT Taskbook
# Web Application for Task Management

# system libraries
import os

# web transaction objects
from bottle import request, response

# HTML request types
from bottle import route, get, put, post, delete, redirect

# web page template processor
from bottle import template

#for css/js
from bottle import static_file
# database library & support
import dataset
from random import seed, randint
import time
import passwords  # file for encrypting the passwords
import taskManager

VERSION=0.1

# development server
PYTHONANYWHERE = ("PYTHONANYWHERE_SITE" in os.environ)

if PYTHONANYWHERE:
	from bottle import default_app
else:
	from bottle import run

# ---------------------------
# user management
# ---------------------------
user_db = dataset.connect('sqlite:///user.db')
seed()

# ---------------------------
# session management
# ---------------------------
session_db = dataset.connect('sqlite:///session.db')

# ---------------------------
# web application routes
# ---------------------------

#so css file works
@route('/static/<filename>')
def send_static(filename):
	return static_file(filename, root='static/')

@route('/')
@route('/tasks')
def tasks():
	session_id = request.cookies.get('session_id', None)
	if session_id:
		session_id = int(session_id)
	else:
		session_id = randint(10000000, 20000000)  # not ideal; want session id to massive
		response.set_cookie('session_id', str(session_id))

	# try to load session information
	session_table = session_db.create_table('session')
	sessions = list(session_table.find(session_id = session_id))
	if len(sessions) == 0:  # need to make a session
		session = {
			"session_id":session_id,
			"started_at":time.time(),
			"username": None,
			"language": "english"
		}
		session_table.insert(session)  # put session into database
	else:
		session = sessions[0]

	if "username" not in session:
		return template(session["language"] + "/login_failure.tpl")
	if session["username"] == None:
		return redirect('/login')

	# persist the session
	session_table.update(row = session, keys = ['session_id'])

	assert session_id
	assert int(session_id)

	#save_session(response, session)
	response.set_cookie('session_id', str(session_id))  # <host/url> <name> <value>
	return template(session["language"] + "/tasks.tpl")


@route('/session')
def session():
	# Displays session info
	session_id = request.cookies.get('session_id', None)
	if session_id:
		session_id = int(session_id)
		session_table = session_db.create_table('session')
		sessions = list(session_table.find(session_id = session_id))
		if len(list(sessions)) > 0:
			session = sessions[0]
		else:
			session = {}
	else:
		session = {}

	return template("session.tpl", session_str = session)


@route('/register')
def register_tpl():
	session_id = request.cookies.get('session_id', None)
	session_table = session_db.create_table('session')
	sessions = list(session_table.find(session_id = session_id))
	if len(sessions) == 0:  # need to make a session
		session = {
			"session_id":session_id,
			"started_at":time.time(),
			"username": None,
			"language": "english"
		}
		session_table.insert(session)  # put session into database
	else:
		session = sessions[0]
	return template(session["language"] + "/register.tpl")


@route('/register', method='POST')
def register():
	# Gets user info from register.tpl
	username = request.forms.get('un')
	password = request.forms.get('pw')
	passwordConfirm = request.forms.get('pwConfirm')

	# Makes sure passwords match
	if password != passwordConfirm:
		return redirect('/register')
	
	session_id = request.cookies.get('session_id', None)
	session_table = session_db.create_table('session')

	# Checks if session exists. If not, create one.
	if session_id:
		session_id = int(session_id)
		sessions = list(session_table.find(session_id = session_id))
		if len(list(sessions)) > 0:
			session = sessions[0]
		else:
			session = {}
	else:
		session_id = randint(10000000, 20000000)  
		session = {
			"session_id":session_id,
			"started_at":time.time(),
			"username": username,
			"language": "english"
		}

	#stores username and encrypted password in db
	user_table = user_db.create_table('user')
	# Checks if username already exists
	for users in user_table:
		if users['username'] == username:
			return redirect('/register')

	# Creates user profile and updates the database
	user_profile = {
		"username": username,
		"language": session["language"],
		"password": passwords.encode_password(password)
	}
	user_table.insert(user_profile)
	# Logs user in immediately after register | Not using
	#session["username"] = username
	#session_table.update(row = session, keys = 'session_id')
	#response.set_cookie('session_id', str(session_id))
	return redirect('/login')


@route("/login")
def login_tpl():
	session_id = request.cookies.get('session_id', None)
	session_table = session_db.create_table('session')
	sessions = list(session_table.find(session_id = session_id))
	if len(sessions) == 0:  # need to make a session
		session = {
			"session_id":session_id,
			"started_at":time.time(),
			"username": None,
			"language": "english"
		}
		session_table.insert(session)  # put session into database
	else:
		session = sessions[0]
	return template(session["language"] + "/login.tpl")


@route("/login", method='POST')
def login():
	session_id = request.cookies.get('session_id', None)
	if session_id:
		session_id = int(session_id)
	else:
		session_id = randint(10000000, 20000000)
	
	#try to load session info
	session_table = session_db.create_table('session')
	sessions = list(session_table.find(session_id = session_id))

	if len(sessions) == 0:
		session = {
			"session_id": session_id,
			"started_at": time.time()
		}
		session_table.insert(session)  # put session into db
	else:
		session = sessions[0]
	
	username = request.forms.get('un')  # Get username and password from login page
	password = request.forms.get('pw')
	user_table = user_db.create_table('user')
	users = list(user_table.find(username = username))

	if len(list(users)) > 0:
		user_profile = list(users)[0]
		if(not passwords.verify_password(password, user_profile["password"])):
			return template(session["language"] + "/login_failure.tpl")
	else:
		return template(session["language"] + "/login_failure.tpl")

	# update the session
	session['username'] = username
	session['language'] = user_profile["language"]

	# persist the session
	session_table.update(row = session, keys = 'session_id')

	response.set_cookie('session_id', str(session_id))  # <host/url> <name> <value>
	return redirect('/tasks')


@route("/logout")
def logout():
	session_id = request.cookies.get('session_id', None)
	if session_id:
		session_id = int(session_id)
	else:
		session_id = randint(10000000, 20000000)
	
	#try to load session info
	session_table = session_db.create_table('session')
	sessions = list(session_table.find(session_id = session_id))

	if len(sessions) == 0:
		session = {
			"session_id": session_id,
			"started_at": time.time()
		}
		session_table.insert(session)  # put session into db
	else:
		session = sessions[0]

	user_table = user_db.create_table('user')
	users = list(user_table.find(username = session["username"]))

	if len(list(users)) > 0:	
		user_profile = list(users)[0]
		user_profile["language"] = session["language"]
		user_table.update(row = user_profile, keys = 'username')

	response.delete_cookie('session_id')
	return redirect('/tasks')


@route("/remove")
def remove_tpl():
	session_id = request.cookies.get('session_id', None)
	session_table = session_db.create_table('session')
	sessions = list(session_table.find(session_id = session_id))
	if len(sessions) == 0:  # need to make a session
		session = {
			"session_id":session_id,
			"started_at":time.time(),
			"username": None,
			"language": "english"
		}
		session_table.insert(session)  # put session into database
	else:
		session = sessions[0]
	return template(session["language"] + "/remove.tpl")


# Delete user account
@route("/remove", method='POST')
def remove():
	# Gets session information from cookie
	session_id = request.cookies.get('session_id', None)
	if session_id:
		session_id = int(session_id)
	else:
		return redirect('/tasks')

	# Load session information
	session_table = session_db.get_table('session')
	sessions = list(session_table.find(session_id = session_id))
	if len(sessions) > 0:
		session = sessions[0]
	else:
		return redirect('/tasks')

	# Gets user info from delete.tpl
	username = request.forms.get('un')
	password = request.forms.get('pw')
	passwordConfirm = request.forms.get('pwConfirm')

	# Gets current user from user.db
	user_table = user_db.get_table('user')
	users = list(user_table.find(username = session["username"]))
	if len(list(users)) > 0:
		user_profile = list(users)[0]
	else:
		return redirect('/login')
	
	# Makes sure a user is logged in | Possibly redundant due to checks when loading session info
	if session["username"] == None:
		return redirect('/tasks')

	if passwordConfirm != password:
		return redirect('/remove')

	if session["username"] != username or not passwords.verify_password(password, user_profile["password"]):
		return redirect('/remove')
	else:
		user_db.query("DELETE FROM user WHERE username = '" + session["username"] + "'")
		taskbook_db.query("DELETE FROM task WHERE user = '" + session["username"] + "'")

	return redirect('/logout')


@route("/english")
def english():
	session_id = request.cookies.get('session_id', None)
	if session_id:
		session_id = int(session_id)
	else:
		session_id = randint(10000000, 20000000)
	
	#try to load session info
	session_table = session_db.create_table('session')
	sessions = list(session_table.find(session_id = session_id))

	if len(sessions) == 0:
		session = {
			"session_id": session_id,
			"started_at": time.time()
		}
		session_table.insert(session)  # put session into db
	else:
		session = sessions[0]
	
	session["language"] = "english"
	session_table.update(row = session, keys = 'session_id')
	
	return redirect("/tasks")


@route("/japanese")
def japanese():
	session_id = request.cookies.get('session_id', None)
	if session_id:
		session_id = int(session_id)
	else:
		session_id = randint(10000000, 20000000)
	
	#try to load session info
	session_table = session_db.create_table('session')
	sessions = list(session_table.find(session_id = session_id))

	if len(sessions) == 0:
		session = {
			"session_id": session_id,
			"started_at": time.time()
		}
		session_table.insert(session)  # put session into db
	else:
		session = sessions[0]

	session['language'] = "japanese"
	session_table.update(row = session, keys = 'session_id')
	
	return redirect("/tasks")


@route("/hindi")
def hindi():
	session_id = request.cookies.get('session_id', None)
	if session_id:
		session_id = int(session_id)
	else:
		session_id = randint(10000000, 20000000)
	
	#try to load session info
	session_table = session_db.create_table('session')
	sessions = list(session_table.find(session_id = session_id))

	if len(sessions) == 0:
		session = {
			"session_id": session_id,
			"started_at": time.time()
		}
		session_table.insert(session)  # put session into db
	else:
		session = sessions[0]

	session["language"] = "hindi"
	session_table.update(row = session, keys = 'session_id')
	
	return redirect("/tasks")


@route('/general')
def general():
    return template("generalTasks.tpl")

# ---------------------------
# task REST api
# ---------------------------

import json
import dataset
import time

taskbook_db = dataset.connect('sqlite:///taskbook.db')

@get('/api/version')
def get_version():
	return { "version":VERSION }


@get('/api/tasks/<day>')
def get_tasks(day):
	#return a list of tasks sorted by submit/modify time
	response.headers['Content-Type'] = 'application/json'
	response.headers['Cache-Control'] = 'no-cache'

	days = [taskManager.getdate_today(), day]
	return taskManager.get_tasks(days)

@get('/api/remember')
def remember_day():
	return taskManager.get_view()

@post('/api/study')
def update_view():
	data = request.json
	print(data)
	taskManager.set_view(data)

@post('/api/tasks')
def create_task():
	#create a new task in the database
	try:
		data = request.json
		for key in data.keys():
			assert key in ["description","list"], f"Illegal key '{key}'"
		assert type(data['description']) is str, "Description is not a string."
		assert len(data['description'].strip()) > 0, "Description is length zero."
		assert data['list'] in ["today","tomorrow"], "List must be 'today' or 'tomorrow'"
	except Exception as e:
		response.status = "400 Bad Request:" + str(e)
		return
	try:
		print("test")
		if data['list'] == 'tomorrow':
			data['list'] = (taskManager.get_view())['savedDate']
		else:
			data['list'] = taskManager.getdate_today()

		taskManager.insert_Tasks(data['description'].strip(), startDt=data['list'])
	except Exception as e:
		response.status="409 Bad Request:"+str(e)
	# return 200 Success
	response.headers['Content-Type'] = 'application/json'
	return json.dumps({'status':200, 'success': True})


@put('/api/tasks')
def update_task():
	'update properties of an existing task in the database'
	try:
		data = request.json
		for key in data.keys():
			assert key in ["id","description","completed"], f"Illegal key '{key}'"
		if "description" in request:
			assert type(data['description']) is str, "Description is not a string."
			assert len(data['description'].strip()) > 0, "Description is length zero."
		if "completed" in request:
			assert type(data['completed']) is bool, "Completed is not a bool."
	except Exception as e:
		response.status="400 Bad Request:"+str(e)
		return
	try:
		# year, month, date, ident = data['id'].split('-')

		#data['id'] = int(ident)

		task_table = taskbook_db.get_table('task')
		task_table.update(row=data, keys=['id'])
	except Exception as e:
		response.status="409 Bad Request:"+str(e)
		return
	# return 200 Success
	response.headers['Content-Type'] = 'application/json'
	return json.dumps({'status':200, 'success': True})


@get('/api/tomorrow')
def get_tomorrow():
	return taskManager.getdate_tomorrow(taskManager.getdate_today())


@get('/api/get_days/<day>')
def get_days(day):
	days = {'today': taskManager.getdate_today(), 'tomorrow': day}
	return days


@delete('/api/tasks')
def delete_task():
	'delete an existing task in the database'
	try:
		data = request.json
	except Exception as e:
		response.status="400 Bad Request:"+str(e)
		return
	try:
		# year, month, date, ident = data['id'].split('-')

		#data['id'] = int(ident)
		task_table = taskbook_db.get_table('task')
		task_table.delete(id=data['id'])
	except Exception as e:
		response.status="409 Bad Request:"+str(e)
		return
	# return 200 Success
	response.headers['Content-Type'] = 'application/json'
	return json.dumps({'success': True})

@put('/api/color_task')
def color_task():
	taskbook_db = dataset.connect('sqlite:///taskbook.db')  
	data = request.json
	task_id = data['task_id']
	task_color = data['task_color']

	keywords = {"colorKey": task_color, "idKey": task_id}
	query = "UPDATE task SET color= :colorKey WHERE id = :idKey"
	taskbook_db.query(query, keywords)

############## Functions for use with the 'General-Tasks' page ################
@get('/api/tasks-gen')
def get_general_tasks():
    'return a list of tasks with endDt = 1970-1-1'
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return taskManager.get_tasks('1970-1-1') #Date that denotes it as general

@post('/api/tasks-gen')
def create_general_task():
    'create a new general task in the database'
    try:
        data = request.json
        for key in data.keys():
            assert key in ["description", "list"], f"Illegal key '{key}'"
        assert type(data['description']) is str, "Description is not a string."
        assert len(data['description'].strip()) > 0, "Description is length zero."
    except Exception as e:
        response.status = "400 Bad Request:" + str(e)
        return
    try:
        taskManager.insert_Tasks(data['description'].strip(), dateList='general', startDt='1970-1-1')
    except Exception as e:
        response.status="409 Bad Request:"+str(e)
    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'status':200, 'success': True})

@put('/api/tasks-gen')
def update_general_task():
    'update properties of an existing general task in the database'
    try:
        data = request.json
        for key in data.keys():
            assert key in ["id","description","completed","list"], f"Illegal key '{key}'"
        assert type(data['id']) is int, f"id '{id}' is not int"
        if "description" in request:
            assert type(data['description']) is str, "Description is not a string."
            assert len(data['description'].strip()) > 0, "Description is length zero."
        if "completed" in request:
            assert type(data['completed']) is bool, "Completed is not a bool."
    except Exception as e:
        response.status="400 Bad Request:"+str(e)
        return
    if 'list' in data:
        data['time'] = time.time()
    try:
        task_table = taskbook_db.get_table('task')
        task_table.update(row=data, keys=['id'])
    except Exception as e:
        response.status="409 Bad Request:"+str(e)
        return
    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'status':200, 'success': True})

@delete('/api/tasks-gen')
def delete_general_task():
    'delete an existing task in the database'
    try:
        data = request.json
        assert type(data['id']) is int, f"id '{id}' is not int"
    except Exception as e:
        response.status="400 Bad Request:"+str(e)
        return
    try:
        task_table = taskbook_db.get_table('task')
        task_table.delete(id=data['id'])
    except Exception as e:
        response.status="409 Bad Request:"+str(e)
        return
    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'success': True})


if PYTHONANYWHERE:
	application = default_app()
else:
	if __name__ == "__main__":
		run(host='localhost', port=8080, debug=True)

