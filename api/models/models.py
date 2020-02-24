from flask_restplus import fields



def create_crypto_fields():
    """ Creates fields for the crypto model

    Returns
    -----
    (dict) : fields of the crypto model
    """
    crypt_field = {
        "_id"        : fields.String(description="The unique identifier of the document"),
        "name"       : fields.String(required=True, description="The name of the cryptocurrency"),
        "timestamp"  : fields.Integer(required=True, description="The crypto data timestamp"),
        "low"        : fields.Float(required=True, description="Lowest price during the bucket interval"),
        "high"       : fields.Float(required=True, description="Highest price during the bucket interval"),
        "open"       : fields.Float(required=True, description="Closing price (first trade) in the bucket interval"),
        "close"      : fields.Float(required=True, description="Opening price (last trade) in the bucket interval"),
        "bucket"     : fields.Integer(required=True, description="the bucket interval of the crypto data"),
        "created_at" : fields.String(required=True, description="Date of creation")
    }

    return crypt_field