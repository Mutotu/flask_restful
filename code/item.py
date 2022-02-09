import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cannot be left blank')
    # this is imported first "decorater". This authenticates first then calls the  methods
    # @jwt_required()
    # def get(self,name):
    #     # for item in items:
    #     #     if item['name'] == name:
    #     #         return item
        
    #     # next => brings the first item in the list
    #     item = next(filter(lambda x:x['name'] == name, items), None)
    #     # return {'item': item}, 200 if item is not None else 404
    #     return {'item': item}, 200 if item else 404
    
    @jwt_required()
    def get(self, name):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        
        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()
        
        # if row:
        #     return {"item":{"name": row[0], "price": row[1]}}
        # return { 'message': 'Item not found'}, 404
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404
    
    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        
        if row:
            return {"item":{"name": row[0], "price": row[1]}}
        return { 'message': 'Item not found'}, 404
    # @jwt_required()
    def post(self, name):
        # force=True => you dont have to give content-type in postman.though it is dangerous.
        # data = request.get_json(force=True)
        # data = request.get_json(silent=True)
        # if next(filter(lambda x:x['name'] == name, items), None) is not None:
        
        ###
        
        # if next(filter(lambda x:x['name'] == name, items), None):
        #     return {'message': 'An item with name "{}" already exists'.format(name)}, 400

        # data = Item.parser.parse_args()
        # # data = request.get_json()
        # item = {'name':name, 'price':data['price']}
        # items.append(item)
        # return item, 201
        #####
        if Item.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400
        
        data = Item.parser_args()
    
        item = {'name': name, 'price': data['price']}
        try:
            self.insert(item)
        except:
            return {"message": "An error occuroed inserting the item."} , 500 # internal server errorr   
        return item, 201
        
    
    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()
        return item, 201
    
    
    
    # @jwt_required()
    def delete(self, name):
        # this says the "items" variable is outer var. If we dont put global var here python is going to throw error becuase it'll think that items beint asssinged items without knowing items is an outer var.
        # global items
        # items = list(filter(lambda x: x['name'] != name, items))
        # return {'message': 'Item deleted'}
    ########
    
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
    
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
    
    
    # @jwt_required()
    def put(self, name):
        # parser = reqparse.RequestParser()
        # parser.add_argument('price', type=float, required=True, help='This field cannot be left blank')
        data =Item.parser.parse_args()
        # print(data)
        # item = next(filter(lambda x:x['name'] == name, items), None)
        item = self.find_by_name(name)
        updated_item  = {'name' : name, 'price': data['price']}
        
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message": "An error occured inserting the item"}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "An error occured updating the item" }, 500
        return item
    
    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))
        
        connection.commit()
        connection.close()
    
class ItemList(Resource):
    
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items  = []
        for row in result:
            items.append({'name':row[0], 'price':row[1]})
        connection.close()
        
        return {'items': items}