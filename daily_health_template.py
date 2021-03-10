import os
import time
import random
import datetime
import encryption
from selenium import webdriver
from datetime import datetime
""" REMOVE COMMENTS TO ENABLE TEXT CONFIRMATION
from twilio.rest import Client
"""

"""
    Requirements: selenium needs to be installed and have a compatible Chrome Version (Link in README.md)

    Description: 
    This simple script uses Selenium in headless mode to automate the Daily Health Screen App. It also saves a
    screenshot in a folder, named after the username used, in the local directory to show it was completed
    All you have to do is fill in your username and password in the 'Info.txt' file
    To automate you can set up task scheduler on windows, or set Loop to True and fill out the desired completion time
    
    Do note that there are some extra features that are commented out for simplicity
    Their function and how to enable them are in the README.md 
"""

Loop = True  # Loops the program every day if True
min_hour = 9  # Earliest hour you want the program to run
max_hour = 11  # Latest hour you want the program to run
File_Name = "Info.txt"  # Name of the file with the user information

""" REMOVE COMMENTS TO ENABLE TEXT CONFIRMATION
account_sid = 
auth_token = 
client = Client(account_sid, auth_token)
"""


def send_text(text):
    """ REMOVE COMMENTS TO ENABLE TEXT CONFIRMATION

    # Message format: (text, Twilio number, target number)
    message = client.messages \
        .create(
            body=text,
            from_='+15555555555',
            to='+15555555555'
        )
    print(message.sid)
    """
    print("Sending Text:\n"+text+"\n")


def sleep_time() -> int:
    year = datetime.today().year
    month = datetime.today().month
    day = datetime.today().day + 1
    hour = random.randint(min_hour, max_hour-1)
    minute = random.randint(0, 59)

    now = datetime.today()
    then = datetime(year, month, day, hour, minute)
    print("Sleeping till ", then)
    return int((then-now).total_seconds())


def folder_check(username):
    path = './' + username + '/'
    if not os.path.exists(path):
        os.makedirs(path)


def complete_form(username, password):
    options = webdriver.ChromeOptions()
    # makes it headless = True
    options.headless = True
    date = datetime.now()
    driver = webdriver.Chrome(executable_path='chromedriver\chromedriver.exe', chrome_options=options)
    driver.get('https://dailyhealth.rit.edu/')
    time.sleep(1)
    # Username
    driver.find_element_by_id('username').send_keys(username)
    # Password
    driver.find_element_by_id('password').send_keys(password)
    time.sleep(1)
    # clicks to login
    driver.find_element_by_xpath("//button[@name='_eventId_proceed']").click()
    time.sleep(2)
    # clicks let's start button
    driver.find_element_by_xpath("//a[@class='c0 c1 at c2 br b2 aq c3 c4 c5 c6 c7 c8']").click()
    time.sleep(2)
    # clicks no
    element = driver.find_element_by_xpath("//div[@class='dc dd de df dg dh di dj ai aj dk br dm dn']")
    driver.execute_script("arguments[0].click();", element)
    # waits for page to load so it can take screenshot of complete submission
    time.sleep(4)
    # takes screenshot and saves to directory of python file
    folder_check(username)
    driver.get_screenshot_as_file(
        username + "/dailyHealthScreen {month}-{day}-{year}.png".format(month=date.month, day=date.day, year=date.year))
    driver.quit()


def complete_group(filename):
    users = encryption.load_file(filename)
    for user in users:
        print("Completing ", user, '\n')
        complete_form(user, users[user].get_password())
        send_text("Completed " + user)


def main():
    complete_group(File_Name)

    # Starts the loop if Loop is True
    while Loop:
        # Waits tills tomorrow's wake up time
        time.sleep(sleep_time())
        print("Running\n")
        complete_group(File_Name)


if __name__ == '__main__':
    main()
