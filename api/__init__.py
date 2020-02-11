from flask_restplus import Api
from .crypto_namespace import ns as cryptoNS


# API constructor
api = Api(
    title = "REST-coin",
    description = "interact with mined cryptocurrencies data",
    version = 1.0
)

# Add namespace
api.add_namespace(cryptoNS)
