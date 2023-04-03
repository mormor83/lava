import json
import requests
from flask import *
import logging
import urllib3
import socket   
import os


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# get the root logger
logger = logging.getLogger()

# create a formatter object
logFormatter = logging.Formatter("%(asctime)s -  %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")


# add console handler to the root logger
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

# add file handler to the root logger
fileHandler = logging.FileHandler("logs.log")
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

app = Flask(__name__)


class InvalidISBNUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidISBNUsage)
def invalid_isbn(e):
    return jsonify(e.to_dict()), e.status_code

@app.route("/")
def hello_world():
    hostname=socket.gethostname()   
    IPAddr=socket.gethostbyname(hostname)
    return render_template('home.html', IPAddr=IPAddr,hostname=hostname)


@app.route('/book')
def book():
    if 'ISBN_NUM' not in request.args :
        no_isbn_message="No ISBN_NUM provided!"
        app.logger.error(no_isbn_message)
        raise InvalidISBNUsage(no_isbn_message)
    search_isbn = request.args.get('ISBN_NUM')
    respond = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:' + str(search_isbn))
    data = json.loads(respond.content)
    if data['totalItems'] == 0:
        no_isbn_found_message="Could not find such ISBN! -> " +str(search_isbn)
        app.logger.error(no_isbn_found_message)
        raise InvalidISBNUsage(no_isbn_found_message, status_code=404)
    book_info = data['items'][0]
    return book_info


app.run()
