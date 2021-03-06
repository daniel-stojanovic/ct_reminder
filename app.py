'''from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__)
api = Api(app)
app.debug=True

class Employees(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from employees") # This line performs query and returns json result
        return {'employees': [i[0] for i in query.cursor.fetchall()]} # Fetches first column that is Employee ID

class Tracks(Resource):
    def get(self):


class Employees_Name(Resource):
    def get(self, employee_id):
        conn = db_connect.connect()
        query = conn.execute("select * from employees where EmployeeId =%d "  %int(employee_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)
    def delete(self,employee_id):
        conn = db_connect.connect()
        query = conn.execute("delete from employees where EmployeeId =%d " % int(employee_id))
        return "deleted employee"  # Fetches first column that is Employee ID


api.add_resource(Employees, '/employees') # Route_1
api.add_resource(Tracks, '/tracks') # Route_2
api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3

@app.route('/')
def index():
    return "Hi Danny5"

if __name__ == '__main__':
    app.run(port='5002')
'''


from flask import Flask
app = Flask(__name__)

@app.route('/')
def display():

    test ="Looks like it works!" + "yay"
    return test

if __name__=='__main__':
    app.run(debug=True, host = '192.168.0.5', port=3134)