from flask_restplus import Namespace, Resource, fields
from datetime import datetime

from configs import mongo


# namespace and its metadata
ns = Namespace('api/cryptocoin', description = 'Cryptocurrencies related operations', endpoint='cryptocoin')
db = mongo.db.coins


#=============================================================
#   MODEL
#=============================================================

crypto = ns.model('Crypto', {
    "id"         : fields.Integer(readonly=True, description="The crypto data unique identifier"),
    "name"       : fields.String(required=True, description="The name of the cryptocurrency"),
    "timestamp"  : fields.Integer(required=True, description="The crypto data timestamp"),
    "low"        : fields.Float(required=True, description="Lowest price during the bucket interval"),
    "high"       : fields.Float(required=True, description="Highest price during the bucket interval"),
    "open"       : fields.Float(required=True, description="Closing price (first trade) in the bucket interval"),
    "close"      : fields.Float(required=True, description="Opening price (last trade) in the bucket interval"),
    "bucket"     : fields.Integer(required=True, description="the bucket interval of the crypto data"),
    "created_at" : fields.String(required=True, description="Date of creation")
    })



#=============================================================
#   DAO
#=============================================================

class CryptoDAO(object):
    """
    """

    def __init__(self):
        """ """
        self.cryptos = []   ## TEMP: temporary database for tests
        self.cpt   = 0    ## TEMP: temporary way to give id


    #---------------------------------------------
    #   BY CRYPTOCURRENCY NAME
    #---------------------------------------------
    def getByName(self, name):
        """Return all data collections related to a cryptocurrency"""
        ret = []
        for crypt in self.cryptos:
            if crypt['name'] == name:
                ret.append(crypt)    
        return ret


    #---------------------------------------------
    #   BY ID
    #---------------------------------------------

    def getByID(self, id):
        """Return data from a crypto"""
        for crypt in self.cryptos:
            if crypt['id'] == id:
                return crypt
        ns.abort(404, "Id {} doesn't exist".format(id), data={})


    def update(self, id, data):
        """Update a data collection"""
        crypto = self.getByID(id)
        crypto.update(data)
        return crypto


    def delete(self, id):
        """Delete a data collection"""
        crypto = self.getByID(id)
        self.cryptos.remove(crypto)


    #---------------------------------------------
    #   COMMON
    #---------------------------------------------

    def getAll(self):
        """
        """
        return db.find({})


    def create(self, data):
        """Create a new data collection"""
        try:
            crypto = data
            crypto['id'] = self.cpt = self.cpt + 1    # auto increment id
            crypto['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.cryptos.append(crypto)
        except TypeError as e:
            print("Error {}".format(e))
        return crypto



# DAO object
DAO = CryptoDAO()





#=============================================================
#   ROUTING
#=============================================================

#---------------------------------------------
#   ALL DATA
#---------------------------------------------
@ns.route("/", strict_slashes = False)     # strict_slashes setted to False so the debuger ignores it
class CryptoList(Resource):
    """
    Get a list of all stored data and allows POST to add new datasets
    """

    @ns.doc('list_deals')
    @ns.marshal_list_with(crypto)
    def get(self):
        """Return a list of all crypto data"""
        return DAO.getAll(), 200

    @ns.doc('create_deal')
    @ns.expect(crypto)
    @ns.marshal_with(crypto, code=201)
    def post(self):
        """Create a new crypto data"""
        return DAO.create(ns.payload), 201


#---------------------------------------------
#   CRUD BY ID
#---------------------------------------------
@ns.route("/<int:id>")
@ns.response(404, 'Crypto data not found')
@ns.param('id', 'The crypto data unique identifier')
class CryptoByID(Resource):
    """
    Show a single data item, update one, or delete one
    """

    @ns.doc('get_crypto_by_id')
    @ns.marshal_with(crypto)
    def get(self, id):
        """Returns a single data collection by id"""
        return DAO.getByID(id), 200


    @ns.doc('update_crypto')
    @ns.marshal_with(crypto)
    def put(self, id):
        """Update a data collection"""
        return DAO.update(id, ns.payload), 204


    @ns.doc('delete_crypto')
    @ns.response(204, 'Crypto deleted')
    def delete(self, id):
        """Delete a data collection"""
        DAO.delete(id)
        return '', 204


#---------------------------------------------
#   CRUD BY CRYPTOCURRENCY'S NAME
#---------------------------------------------
@ns.route("/<string:name>")
@ns.response(404, 'Crypto data not found')
@ns.param('name', 'The name of the cryptocurrency')
class CryptoByName(Resource):
    """
    Show a single data item, update one, or delete one
    """

    @ns.doc('get_crypto_by_name')
    @ns.marshal_with(crypto)
    def get(self, name):
        """Returns all data collections related to a cryptocurrency"""
        return DAO.getByName(name), 200
