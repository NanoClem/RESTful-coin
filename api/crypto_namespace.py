from flask_restplus import Namespace, Resource, fields
from datetime import datetime
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson.errors import InvalidId

from configs import mongo
from api.models import create_crypto_model


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

class CryptoDAO(object):
    """
    """

    #---------------------------------------------
    #   BY CRYPTOCURRENCY NAME
    #---------------------------------------------
    def getByName(self, name):
        """Return all data collections related to a cryptocurrency
        
        Parameter
        -----
        name (string) : the cryptocurrency's name
        """
        cursor = list(db.find({'name': name}))
        if cursor :
            return cursor
        ns.abort(404, "cryptocurrency {} doesn't exist".format(name), data={})


    #---------------------------------------------
    #   BY ID
    #---------------------------------------------

    def getByID(self, id):
        """Return data from a crypto

        Parameter
        ----
        id (int) : the document unique id
        
        """
        try:
            data = db.find_one({"_id": ObjectId(id)})
            if data != None:
                return data
            ns.abort(404, "Id {} doesn't exist".format(id), data={})
        except InvalidId:
            ns.abort(422, "Invalid id {}".format(id), data={})
        

    def update(self, id, data):
        """Update a data collection"""
        crypto = self.getByID(id)
        db.update_one(crypto, data)


    def delete(self, id):
        """Delete a data collection"""
        data = self.getByID(id)
        print(data)
        db.delete_one(data)


    #---------------------------------------------
    #   COMMON
    #---------------------------------------------

    def exists(self, data):
        """ Check if a document already exists in collection

        Parameter
        -----
        data (dict, json): document to check

        Returns
        -----
        True if exists, else False
        """
        return db.count_documents(data, limit = 1) != 0


    def getAll(self):
        """ Get all documents in database """
        cursor = db.find({})
        return list(cursor)


    def create(self, data):
        """ Create a new data document """
        if self.exists(data):
            ns.abort(409, "document already exists", data={})
        else:
            data['created_at'] = datetime.now()
            db.insert(data)
            return data


    def createMany(self, dataList):
        """ Create multiple data documents
        """
        temp = dataList
        # PRE-PROCESS DATA IN LIST
        for data in dataList:
            if self.exists(data):
                temp.remove(data)
            else:
                data['created_at'] = datetime.now()
        
        db.insert_many(temp)
        return temp
        


# DAO object
DAO = CryptoDAO()





#=============================================================
#   ROUTING
#=============================================================

#---------------------------------------------
#   MANY DATA
#---------------------------------------------
@ns.route("/cryptocoins", strict_slashes = False)     # strict_slashes setted to False so the debuger ignores it
class CryptoList(Resource):
    """
    Get a list of all stored data and allows POST to add new datasets
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
#   ONE DATA
#---------------------------------------------
@ns.route("/cryptocoin", strict_slashes = False)
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
@ns.route("/cryptocoin/<string:id>")
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
@ns.route("/cryptocoins/<string:name>")
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
