from flask import request
from functools import wraps


# ELEMENTS REQUIRED TO ACCESS SOME PART OF THE APi
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}



# WRAPER FOR AUTHENTICATION
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None
        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']

        if not token:
            return {'message': 'token is missing'}, 401

        if token != 'testToken':
            return {'message': 'wrong token'}, 401

        print('TOKEN : {}'.format(token))
        return f(*args, **kwargs)
    
    return decorated