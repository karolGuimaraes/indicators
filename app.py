from flask import Flask
from indicators.views import main

app = Flask(__name__)

if __name__ == '__main__':
    main()