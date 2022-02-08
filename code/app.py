from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):
    
    def get(self,name):
        # for item in items:
        #     if item['name'] == name:
        #         return item
        
        # next => brings the first item in the list
        item = next(filter(lambda x:x['name'] == name, items), None)
        # return {'item': item}, 200 if item is not None else 404
        return {'item': item}, 200 if item else 404
    
    def post(self, name):
        # force=True => you dont have to give content-type in postman.though it is dangerous.
        # data = request.get_json(force=True)
        # data = request.get_json(silent=True)
        # if next(filter(lambda x:x['name'] == name, items), None) is not None:
        if next(filter(lambda x:x['name'] == name, items), None):
            return {'message': 'An item with name "{}" already exists'.format(name)}, 400

        data = request.get_json()
        item = {'name':name, 'price':data['price']}
        items.append(item)
        return item, 201
    
    
class ItemList(Resource):
    
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
app.run(port=5000, debug=True) 