from behave_webdriver.steps import *
from behave import *
from selenium import webdriver

def before_all(context):
    context.browser = webdriver.Chrome()