from flask_restplus import Api
from .crypto_namespace import ns as ns_crypto


# API constructor
api = Api(
    title = "REST-coin",
    description = "interact with mined cryptocurrencies data",
    version = 1.0
)


def register_api(app):
    """ Registering namespaces and the api to the app
    """
    api.add_namespace(ns_crypto)  # Add namespace
    api.init_app(app)
