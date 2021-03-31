# SWIFT Taskbook
# Web Application for Task Management

# system libraries
import os
import taskManager

# web transaction objects
from bottle import request, response

# HTML request types
from bottle import route, get, put, post, delete

# web page template processor
from bottle import template

VERSION=0.1

# development server
PYTHONANYWHERE = ("PYTHONANYWHERE_SITE" in os.environ)

if PYTHONANYWHERE:
    from bottle import default_app
else:
    from bottle import run

# ---------------------------
# web application routes
# ---------------------------

@route('/')
@route('/tasks')
def tasks():
    return template("tasks.tpl")

@route('/login')
def login():
    return template("login.tpl")

@route('/register')
def login():
    return template("register.tpl")

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
    'return a list of tasks sorted by submit/modify time'
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
    'create a new task in the database'
    try:
        data = request.json
        assert type(data['description']) is str, "Description is not a string."
        assert len(data['description'].strip()) > 0, "Description is length zero."
    except Exception as e:
        response.status = "400 Bad Request:" + str(e)
        return
    try:
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
        year, month, date, ident = data['id'].split('-')

        data['id'] = int(ident)

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
        year, month, date, ident = data['id'].split('-')

        data['id'] = int(ident)
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


