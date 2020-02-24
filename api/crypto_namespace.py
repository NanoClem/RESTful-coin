from flask_restplus import Namespace, Resource, fields
from datetime import datetime
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson.errors import InvalidId

from configs import mongo
from api.models import create_crypto_model
from api.DAO import CryptoDAO


# namespace and its metadata
ns = Namespace('api', description = 'Cryptocurrencies related operations', endpoint='cryptocoin')
db = mongo.db.coins


#=============================================================
#   MODEL
#=============================================================
crypto = create_crypto_model(ns)


#=============================================================
#   DAO
#=============================================================
DAO = CryptoDAO(db, ns)


#=============================================================
#   ROUTING
#=============================================================
single_route = "/cryptocoin"
many_route   = "/cryptocoins"

#---------------------------------------------
#   MANY DATA
#---------------------------------------------
@ns.route(many_route, strict_slashes = False)     # strict_slashes setted to False so the debuger ignores it
class CryptoList(Resource):
    """
    Get a list of all stored data and allows POST for multiple documents
    """

    @ns.doc('get all collections')
    @ns.marshal_list_with(crypto)
    def get(self):
        """Return a list of all crypto data"""
        return DAO.getAll(), 200


    @ns.doc('create many collections')
    @ns.expect(crypto)
    @ns.marshal_list_with(crypto, code=201)
    def post(self):
        """Create multiple crypto data records"""
        return DAO.createMany(ns.payload), 201


#---------------------------------------------
#   POST ONE DATA
#---------------------------------------------
@ns.route(single_route, strict_slashes = False)
class Crypto(Resource):
    """
    """

    @ns.doc('create one collection')
    @ns.expect(crypto)
    @ns.marshal_with(crypto, code=201)
    def post(self):
        """Create a new crypto data"""
        return DAO.create(ns.payload), 201


#---------------------------------------------
#   CRUD BY ID
#---------------------------------------------
@ns.route(single_route + "/<string:id>")
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
        DAO.update(id, ns.payload)
        return '', 204


    @ns.doc('delete_crypto')
    @ns.response(204, 'Crypto deleted')
    def delete(self, id):
        """Delete a data collection"""
        DAO.delete(id)
        return '', 204


#---------------------------------------------
#   CRUD BY CRYPTOCURRENCY'S NAME
#---------------------------------------------
@ns.route(many_route + "/<string:name>")
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
