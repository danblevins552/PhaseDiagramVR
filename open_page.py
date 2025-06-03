# This file is necessary because of localtunnel's stupid landing page and the random URLs
# If we want a more polished tool in the future, we will need to make a basic app for the Quest

import os
import time
import pickle

def open_webpage_on_metaquest(url, password, adb_path=""):
    """
    Opens a webpage on MetaQuest and enters a password using ADB commands.

    Parameters:
    - url (str): The URL to open.
    - password (str): The password to enter on the webpage.
    - adb_path (str): The full path to the ADB executable on Windows.
    """
    try:
        os.system(f'"{adb_path}" shell am start -a android.intent.action.VIEW -d "{url}"')
        time.sleep(4)
        os.system(f'"{adb_path}" shell input keyevent 61')
        time.sleep(0.5)
        os.system(f'"{adb_path}" shell input keyevent 61')
        time.sleep(0.5)
        
        for i in password:
            os.system(f'"{adb_path}" shell input text "{i}"')
            time.sleep(0.02)

        os.system(f'"{adb_path}" shell input keyevent 66')
        
    except Exception as e:
        print(f"An error occurred: {e}")