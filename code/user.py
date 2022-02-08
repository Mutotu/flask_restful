import sqlite3
from flask_restful import Resource, reqparse

class User:
    
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password
    
    
    # @classmethod, cls => calls the class name > User so instead use cls ...
    @classmethod    
    def find_by_username(cls, username):
        # after importing sqlite3, call the methods ..conncect(), cursor(), exceute(), close(),commit()...
        
        # creates and connects to database
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,)) # coma has to be at the end to make it validated
        row = result.fetchone()
        if row:
            # below is an alternative to cls(*row)
            # user = cls(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user
    
    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM users WHERE id=?"
        
        result = cursor.execute(query, (_id,))
        row= result.fetchone()
        
        if row:
            user =cls(*row)
        else:
            user = None
        connection.close()
        return user
    
    


# create a user
class UserRegister(Resource):
    
    #reqparse => creates constrains => parser.add_argument(....)
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be blank")
    parser.add_argument('password', type=str, required=True, help="This field cannot be blank")
    
    def post(self):
        # USerRegister.parser is the variable in the class not in the methods.
        data = UserRegister.parser.parse_args()
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))
        
        connection.commit()
        connection.close()
        
        return {"message": "user created succesfully"}, 201