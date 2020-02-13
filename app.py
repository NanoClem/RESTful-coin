from flask import Flask

from api import register_api
from configs import settings as stg
from configs import app




if __name__ == '__main__':
    
    register_api(app)
    app.run(host=stg.HOST, port=stg.PORT, debug=stg.DEBUG)