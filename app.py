from flask import Flask
from api import api
import settings as stg


if __name__ == '__main__':

    # SETTINGS
    host = stg.HOST
    port = stg.PORT

    # INIT APP
    app = Flask(__name__)
    api.init_app(app)

    app.run(host=host, port=port, debug=stg.DEBUG)
