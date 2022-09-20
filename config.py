from os import getenv
from dotenv import load_dotenv
load_dotenv()

class Config:
    APP_PORT = int(getenv('APP_PORT'))
    DEBUG = eval(getenv('DEBUG').title())