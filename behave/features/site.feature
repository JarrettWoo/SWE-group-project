Feature: Taskbook Website

    Scenario: Accessing Taskbook
        Given we can access taskbook
        When  we visit the URL for the project
        Then  we get the taskbook page

    Scenario: Sign-In to Taskbook
        Given we can access taskbook
        When  we input our credentials
        Then  we are signed in

    Scenario: Create a Task
        Given we can access taskbook
        And   we are signed in
        When  we make a task
        Then  the task is available