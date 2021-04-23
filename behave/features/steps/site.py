#from behave_webdriver.steps import *
from behave import *
import requests
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

@when(u'we make a task')
def step_impl(context):
    context.payload = {
        'input-today': 'test task'
    }
    context.r = context.s.post('http://bbehnkese.pythonanywhere.com/tasks', data=context.payload)

@then(u'the task is available')
def step_impl(context):
    bs = BeautifulSoup(context.r.text)

@when(u'we input our credentials')
def step_impl(context):
    context.s = requests.Session()
    context.payload = {
        'un': 'test',
        'pw': 'test'
    }
    context.LogIn = context.s.post('http://bbehnkese.pythonanywhere.com/login', data=context.payload)

@then(u'we are signed in')
def step_impl(context):
    bs = BeautifulSoup(context.LogIn.text, 'html.parser')
    if "w3-row taskbook-container" in bs:
        print('Pass.')
    else:
        print('Fail.')

@given(u'we are signed in')
def step_impl(context):
    context.r = requests.get('http://bbehnkese.pythonanywhere.com/tasks')
    assert(context.r.status_code == 200)
