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
    print("session_id =", session_id)
    if session_id:
        session_id = int(session_id)
    else:
        session_id = randint(10000000, 20000000)  # not ideal; want session id to massive
    
    # try to load session information
    session_table = session_db.create_table('session')
    sessions = list(session_table.find(session_id = session_id))
    if len(sessions) == 0:  # need to make a session
        session = {
            "session_id":session_id,
            "started_at":time.time(),
            "username": None
        }
        session_table.insert(session)  # put session into database
    else:
        session = sessions[0]

    print("Logged in as", session["username"])
    if "username" not in session:
        return template("login_failure.tpl", user = "not logged in", password = "n/a")
    if session["username"] == None:
        return redirect('/login')

    # persist the session
    session_table.update(row = session, keys = ['session_id'])

    assert session_id
    assert int(session_id)

    #save_session(response, session)
    response.set_cookie('session_id', str(session_id))  # <host/url> <name> <value>
    return template("tasks.tpl")


@route('/session')
def session():
    # Displays session info
    session_id = request.cookies.get('session_id', None)
    print("sesson_id in request =", session_id)
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
    return template('register.tpl')

@route('/register', method='POST')
def register():
    # Gets user info from register.tpl
    username = request.forms.get('un')
    password = request.forms.get('pw')
    passwordConfirm = request.forms.get('pwConfirm')

    # Makes sure passwords match
    if password != passwordConfirm:
        print("Passwords do not match!")
        return redirect('/register')
    
    print("registering", username, password)
    session_id = request.cookies.get('session_id', None)
    print("sesson_id in request =", session_id)
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
            "username": username
        }

    #stores username and encrypted password in db
    user_table = user_db.create_table('user')
    # Checks if username already exists
    for users in user_table:
        if users['username'] == username:
            print("Name already in use!")
            return redirect('/register')

    # Creates user profile and updates the cookie
    user_profile = {
        "username": username,
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
    return template("login.tpl")


@route("/login", method='POST')
def login():
    username = request.forms.get('un')  # get username and password from login.tpl
    password = request.forms.get('pw')
    print(username)
    user_table = user_db.create_table('user')
    users = list(user_table.find(username = username))

    if len(list(users)) > 0:
        user_profile = list(users)[0]
        print("user_profile:", user_profile)
        if(not passwords.verify_password(password, user_profile["password"])):
            return template("login_failure.tpl",user=username, password="****")
    else:
        return template("login_failure.tpl",user=username, password="****")

    session_id = request.cookies.get('session_id', None)
    print("session_id in request = ", session_id)
    if session_id:
        session_id = int(session_id)
    else:
        print("getting new session from randint")
        session_id = randint(10000000, 20000000)
    print("Login", username, session_id)

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

    # update the session
    session['username'] = username
    print("update the session", session)

    # persist the session
    session_table.update(row = session, keys = 'session_id')
    print("persisting cookie as", username, session_id)

    response.set_cookie('session_id', str(session_id))  # <host/url> <name> <value>
    return redirect('/tasks')


@route("/logout")
def logout():
    print("logging out...")
    response.delete_cookie('session_id')
    return redirect('/tasks')


@route("/remove")
def remove_tpl():
    return template("remove.tpl")


# Delete user account
@route("/remove", method='POST')
def remove():
    # Gets session information from cookie
    session_id = request.cookies.get('session_id', None)
    if session_id:
        session_id = int(session_id)
    else:
        print("No session in cookie.")
        return redirect('/tasks')

    # Load session information
    session_table = session_db.get_table('session')
    sessions = list(session_table.find(session_id = session_id))
    if len(sessions) > 0:
        session = sessions[0]
    else:
        print("No session in table.")
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
        print("No users")
        return redirect('/login')
    
    # Makes sure a user is logged in | Possibly redundant due to checks when loading session info
    if session["username"] == None:
        print("No account logged in. Redirecting to homepage...")
        return redirect('/tasks')

    if passwordConfirm != password:
        print("Passwords do not match!")
        return redirect('/remove')

    if session["username"] != username or not passwords.verify_password(password, user_profile["password"]):
        print("Unable to verify account.")
        return redirect('/remove')
    else:
        user_db.query("DELETE FROM user WHERE username = '" + session["username"] + "'")
        taskbook_db.query("DELETE FROM task WHERE user = '" + session["username"] + "'")

    return redirect('/logout')


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


@get('/api/tasks')
def get_tasks():
    'return a list of tasks sorted by submit/modify time'
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    # task_table = taskbook_db.get_table('task')
    # tasks = [dict(x) for x in task_table.find()]
    # return { "tasks": tasks }

    return taskManager.get_tasks(taskManager.getdate_today())

@post('/api/tasks')
def create_task():
	'create a new task in the database'
	try:
		data = request.json
		for key in data.keys():
			assert key in ["description","list"], f"Illegal key '{key}'"
		assert type(data['description']) is str, "Description is not a string."
		assert len(data['description'].strip()) > 0, "Description is length zero."
		assert data['list'] in ["today","tomorrow"], "List must be 'today' or 'tomorrow'"
	except Exception as e:
		response.status="400 Bad Request:"+str(e)
		return
	try:
		taskManager.insert_Tasks(data['description'].strip(), dateList=data['list'])
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
			assert key in ["id","description","completed","list"], f"Illegal key '{key}'"
		assert type(data['id']) is int, f"id '{id}' is not int"
		if "description" in request:
			assert type(data['description']) is str, "Description is not a string."
			assert len(data['description'].strip()) > 0, "Description is length zero."
		if "completed" in request:
			assert type(data['completed']) is bool, "Completed is not a bool."
		if "list" in request:
			assert data['list'] in ["today","tomorrow"], "List must be 'today' or 'tomorrow'"
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

@delete('/api/tasks')
def delete_task():
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

import dataset

@put('/api/color_task')
def color_task():
	taskbook_db = dataset.connect('sqlite:///taskbook.db')  
	data = request.json
	task_id = data['task_id']
	task_color = data['task_color']

	keywords = {"colorKey": task_color, "idKey": task_id}
	query = "UPDATE task SET color= :colorKey WHERE id = :idKey"
	taskbook_db.query(query, keywords)

if PYTHONANYWHERE:
	application = default_app()
else:
	if __name__ == "__main__":
		run(host='localhost', port=8080, debug=True)


