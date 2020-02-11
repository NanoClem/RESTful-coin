import os
from datetime import datetime
from dotenv import load_dotenv


load_dotenv('.env')

# API
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

# MONGO
MONGO_DBNAME = os.getenv('MONGO_DBNAME')
MONGO_URI    = os.getenv('MONGO_URI')
DEBUG        = True