from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

# notice importingfrom the file security..
from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
app.secret_key = 'muto'
api = Api(app)

jwt = JWT(app, authenticate,identity)  #/auth

items = []

class Item(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cannot be left blank')
    # this is imported first "decorater". This authenticates first then calls the  methods
    @jwt_required()
    def get(self,name):
        # for item in items:
        #     if item['name'] == name:
        #         return item
        
        # next => brings the first item in the list
        item = next(filter(lambda x:x['name'] == name, items), None)
        # return {'item': item}, 200 if item is not None else 404
        return {'item': item}, 200 if item else 404
    # @jwt_required()
    def post(self, name):
        # force=True => you dont have to give content-type in postman.though it is dangerous.
        # data = request.get_json(force=True)
        # data = request.get_json(silent=True)
        # if next(filter(lambda x:x['name'] == name, items), None) is not None:
        
        ###
        
        if next(filter(lambda x:x['name'] == name, items), None):
            return {'message': 'An item with name "{}" already exists'.format(name)}, 400

        data = Item.parser.parse_args()
        # data = request.get_json()
        item = {'name':name, 'price':data['price']}
        items.append(item)
        return item, 201
        #####
      
    
    
    
    # @jwt_required()
    def delete(self, name):
        # this says the "items" variable is outer var. If we dont put global var here python is going to throw error becuase it'll think that items beint asssinged items without knowing items is an outer var.
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}
    
    # @jwt_required()
    def put(self, name):
        # parser = reqparse.RequestParser()
        # parser.add_argument('price', type=float, required=True, help='This field cannot be left blank')
        data =Item.parser.parse_args()
        # print(data)
        item = next(filter(lambda x:x['name'] == name, items), None)
        if item is None:
            item = {'name':name, 'price':data['price']}
            items.append(item)
        else:
            item.update(data)
        return item
    
    
class ItemList(Resource):
    
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


app.run(port=5000, debug=True) 