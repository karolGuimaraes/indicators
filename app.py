from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    host = '0.0.0.0'
    app.run(host=host, port=5000, debug=True)