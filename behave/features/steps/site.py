# features/steps/webdriver_example.py
from behave_webdriver.steps import *
from behave import *
import requests

@given(u'we can access taskbook')
def step_impl(context):
    context.browser.get('http://bbehnkese.pythonanywhere.com/')

@when(u'we visit the URL for the project')
def step_impl(context):
    pass #previous step accounts for this


@then(u'we get the taskbook page')
def step_impl(context):
    pass