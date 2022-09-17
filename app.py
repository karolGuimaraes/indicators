from flask import Flask
from os import getenv
from dotenv import load_dotenv
load_dotenv()

APP_PORT = int(getenv('APP_PORT'))
DEBUG = eval(getenv('DEBUG').title())

app = Flask(__name__)

if __name__ == '__main__':
    host = '0.0.0.0'
    debug = DEBUG
    port = APP_PORT
    app.run(host=host, port=port, debug=debug)