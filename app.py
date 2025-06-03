from serve_local_app import *
from open_page import *

from flask import Flask, render_template
import time

# define the port you want to serve the webpage on
port = 5000

# create a new Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # serve the Flask app on its own thread
    flask_thread = run_flask_app(app, port)

    # # allow some time for the Flask app to start before opening the port to the world
    # time.sleep(1)
    # lt_thread, url = open_port(port)

    # get the password
    # password = fetch_password_with_retry()

    # open the page on the quest
    # open_webpage_on_metaquest(url, password, adb_path=r"/mnt/c/platform-tools-latest-windows/platform-tools/adb.exe")

    # keep the threads alive
    flask_thread.join()
    # lt_thread.join()