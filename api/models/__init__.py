from api.models.models import create_crypto_fields



def create_crypto_model(ns):
    """ Create a model for the given namespace

    Parameter
    -----
    ns (Namespace) : the namespace on which the model is applied

    Returns
    -----
    (Model) : the resulting model of the namespace
    """
    return ns.model('Crypto', create_crypto_fields())