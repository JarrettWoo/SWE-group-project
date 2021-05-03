#from behave_webdriver.steps import *
from behave import *
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup

@given(u'we can access taskbook')
def step_impl(context):
    context.r = requests.get('http://bbehnkese.pythonanywhere.com/login', allow_redirects=False)

@when(u'we visit the URL for the project')
def step_impl(context):
    pass #previous step accounts for this, could change it

@then(u'we get the login page')
def step_impl(context):
    assert(context.r.status_code == 200)

@when(u'we input our credentials')
def step_impl(context):
    context.s = requests.Session()
    context.payload = {
        'un': 'test2',
        'pw': 'test2'
    }
    context.LogIn = context.s.post('http://bbehnkese.pythonanywhere.com/login', data=context.payload, allow_redirects=False)

@then(u'we are signed in')
def step_impl(context):
    context.LogIn = context.s.get('http://bbehnkese.pythonanywhere.com/tasks', allow_redirects=False)
    assert(context.LogIn.status_code == 200)

@given(u'we are signed in')
def step_impl(context):
    context.session = HTMLSession()
    context.payload = {
        'un': 'test2',
        'pw': 'test2'
    }
    r = context.session.post('http://bbehnkese.pythonanywhere.com/login', data=context.payload)
    r2 = context.session.get('http://bbehnkese.pythonanywhere.com/tasks', allow_redirects=False)
    assert(r.status_code == 200)

@when(u'we make a task')
def step_impl(context):
    #context.session = HTMLSession()
    #context.payload = {
    #    'un': 'test',
    #    'pw': 'test'
    #}
    #r = context.session.post('http://bbehnkese.pythonanywhere.com/login', data=context.payload)
    parameters = "test task"
    payload = {"tasks": [{"user": "test2", "description": "test task"}]}
    tt = context.session.post('http://bbehnkese.pythonanywhere.com/api/tasks/two_day', data=payload, json=payload, allow_redirects=False)
    #print(tt.text)
    #print('\n')

@then(u'the task is available')
def step_impl(context):
    #raise NotImplementedError(u'STEP: Then the task is available')
    r = context.session.get('http://bbehnkese.pythonanywhere.com/api/tasks/2021-5-3/two_day', allow_redirects=False)
    assert("test task" in r.text)
    #print(r.text)
    #print('\n')

@given(u'we can access lightsail')
def step_impl(context):
    #raise NotImplementedError(u'STEP: Given we can access lightsail')
    context.session2 = HTMLSession()
    r = context.session2.get('http://3.19.37.101:8080/login')

@when(u'we sign in')
def step_impl(context):
    #raise NotImplementedError(u'STEP: When we sign in')
    context.payload = {
        'un': 'test',
        'pw': 'test'
    }
    r = context.session2.post('http://3.19.37.101:8080/login', data=context.payload)

@then(u'we access taskbook page')
def step_impl(context):
    r = context.session2.get('http://3.19.37.101:8080/tasks', allow_redirects=False)
    assert(r.status_code == 200)

@then(u'we create a task')
def step_impl(context):
    #raise NotImplementedError(u'STEP: Then we create a task')
    parameters = {
        'task': "test task"
    }
    payload = {
        'task': "test task"
    }
    tt = context.session2.post('http://3.19.37.101:8080/api/tasks', data=payload, verify=False, allow_redirects=False)
    #print(tt.text)
    #print('\n')

@then(u'the lightsail task is available')
def step_impl(context):
    #raise NotImplementedError(u'STEP: Then the lightsail task is available')
    r = context.session2.get('http://3.19.37.101:8080/api/tasks/2021-5-7', verify=False, allow_redirects=False) #Accessing 2021-5-7 on 2021-5-1 returns the 1st's tasks
    assert("test task" in r.text)
    #print(r.text)
    #print('\n')
