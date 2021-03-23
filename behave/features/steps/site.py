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
    context.r.status_code

@when(u'we make a task')
def step_impl(context):
    raise NotImplementedError(u'STEP: When we make a task')

@then(u'the task is available')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the task is available')
