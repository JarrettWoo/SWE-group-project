from behave import *
from selenium import webdriver
from pyvirtualdisplay import Display
#import chromedriver

def before_feature(context, site):
    with Display():
        context.browser = webdriver.Chrome()

def after_feature(context, site):
    context.browser.quit()