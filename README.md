# daily_health_screen_automation
An automated selenium web script to automate the daily health screen app from RIT.


By: Thomas Flaglor and Kyle Baptiste

Requirements: selenium needs to be installed and have a compatible Chrome Version (Link in below)

Description: This simple script uses Selenium in headless mode to automate the Daily Health Screen App.
It also saves a screenshot in a folder, named after the username used, in the local directory to show it was completed.
All you have to do is run encryption.py, then you will be able to input your username and password.
You will also be able to create your own encryption formula, or let the program create a random one. 
If there is multiple entries in the text file it will fill out the form for all of them.
To automate you can set up task scheduler on windows, or set Loop to True and fill out the desired completion time

Do note that there are some extra features that are commented out for simplicity.
Their function and how to enable them is listed below.

# Extra Features
+ Self Looping
  - When "Loop" is set to true the program will complete the program, then wait till the next desired time
    - min_hour: Earliest hour you want the program to run (9 - default)
    - max_hour: Latest hour you want the program to run (11 - default)
+ Text confirmation
  - Using Twilio, the program can send a confirmation text to a designated number
    - A Twilio account will have to be created to get a number and client information
    - https://www.twilio.com/

# Notes:
- The program might need a new version for the chrome driver
    - https://chromedriver.chromium.org/downloads
- When creating your free Twilio account you should be given a trail budget
    - This will cover the cost of getting a number, and sending the confirmation texts
    
