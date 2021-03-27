#from behave_webdriver.steps import *
from behave import *
import requests

@given(u'we can access taskbook')
def step_impl(context):
    context.r = requests.get('http://bbehnkese.pythonanywhere.com/')

@when(u'we visit the URL for the project')
def step_impl(context):
    pass #previous step accounts for this, could change it

@then(u'we get the taskbook page')
def step_impl(context):
    assert(context.r.status_code == 200)

@when(u'we make a task')
def step_impl(context):
    context.payload = {
        'input-today': 'test task'
    }
    context.r = requests.post('http://bbehnkese.pythonanywhere.com/tasks', data=context.payload)

@then(u'the task is available')
def step_impl(context):
    #assert(context.r.status_code == 200)
    pass #tasks need to be available first

@when(u'we input our credentials')
def step_impl(context):
    context.payload = {
        'Username': 'test',
        'Password': 'test'
    }
    context.LogIn = requests.post('http://bbehnkese.pythonanywhere.com/login', data=context.payload)

@then(u'we are signed in')
def step_impl(context):
    assert(context.LogIn.status_code == 200)

@given(u'we are signed in')
def step_impl(context):
    context.r = requests.get('http://bbehnkese.pythonanywhere.com/tasks')
    assert(context.r.status_code == 200)
