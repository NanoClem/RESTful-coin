from flask_restplus import Namespace, Resource, fields
from datetime import datetime

# namespace and its metadata
ns = Namespace('api/cyptocoin', description = 'Cryptocurrencies related operations')



#=============================================================
#   MODEL
#=============================================================

crypto = ns.model('Crypto', {
    "id"         : fields.Integer(readonly=True, description="The crypto data unique identifier"),
    "url"        : fields.String(required=True, description="The crypto data url"),
    "created_at" : fields.String(required=True, description="Date of creation")
    })



#=============================================================
#   DAO
#=============================================================

class CryptoModel(object):
    """
    """

    def __init__(self):
        """ """
        self.cryptos = []   ## TEMP: temporary database for tests
        self.cpt   = 0    ## TEMP: temporary way to give id


    def get(self, id):
        """Return data from a crypto"""
        for deal in self.cryptos:
            if deal['id'] == id:
                return deal
        ns.abort(404, "Deal {} doesn't exist".format(id), data={})


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


    def update(self, id, data):
        """Update a data collection"""
        crypto = self.get(id)
        crypto.update(data)
        return crypto


    def delete(self, id):
        """Delete a data collection"""
        crypto = self.get(id)
        self.cryptos.remove(crypto)


# DAO object
DAO = CryptoModel()



#=============================================================
#   ROUTING
#=============================================================

#---------------------------------------------
#   DATA LIST
#---------------------------------------------
@ns.route("/", strict_slashes = False)     # strict_slashes setted to False so the debuger ignores it
class DataList(Resource):
    """
    Get a list of all stored data and allows POST to add new datasets
    """

    @ns.doc('list_deals')
    @ns.marshal_list_with(crypto)
    def get(self):
        """Return a list of all crypto data"""
        return DAO.cryptos, 200

    @ns.doc('create_deal')
    @ns.expect(crypto)
    @ns.marshal_with(crypto, code=201)
    def post(self):
        """Create a new crypto data"""
        return DAO.create(ns.payload), 201


#---------------------------------------------
#   CRUD
#---------------------------------------------
@ns.route("/<int:id>")
@ns.response(404, 'Crypto data not found')
@ns.param('id', 'The crypto data unique identifier')
class Data(Resource):
    """
    Show a single data item, update one, or delete one
    """

    @ns.doc('get_crypto')
    @ns.marshal_with(crypto)
    def get(self, id):
        """Return a single data collection"""
        return DAO.get(id), 200

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
