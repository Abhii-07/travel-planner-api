from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
import os

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgres://wanderlust_db_kv6b_user:H4TfcxmDUZShtZs9YChZsKvCJb3pntAM@dpg-cl72uv8icrhc73d0ge10-a.oregon-postgres.render.com/wanderlust_db_kv6b')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/wanderlust_backend_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['LOG_WITH_GUNICORN'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)
api = Api(app)

# Models
class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    location = db.Column(db.String(255), nullable=False)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)

class Itinerary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)
    activity = db.Column(db.String(255), nullable=False)

# Resource classes
class HelloWorld(Resource):
    def get(self):
        return jsonify({'message': 'Hello, World!'})

class DestinationResource(Resource):
    def get(self):
        destinations = Destination.query.all()
        destination_list = []
        for destination in destinations:
            destination_dict = {
                'id': destination.id,
                'name': destination.name,
                'description': destination.description,
                'location': destination.location
            }
            destination_list.append(destination_dict)
        return jsonify(destination_list)

    def post(self):
        data = request.json
        destination = Destination(name=data['name'], description=data.get('description'), location=data.get('location'))
        db.session.add(destination)
        db.session.commit()
        return jsonify({'message': 'Destination created successfully'})

class DestinationDetailResource(Resource):
    def get(self, destination_id):
        destination = Destination.query.get(destination_id)
        if destination is not None:
            destination_data = {
                'id': destination.id,
                'name': destination.name,
                'description': destination.description,
                'location': destination.location
            }
            return jsonify(destination_data)
        return jsonify({'message': 'Destination not found'}, 404)

    def put(self, destination_id):
        destination = Destination.query.get(destination_id)
        if destination is not None:
            data = request.json
            destination.name = data['name']
            destination.description = data.get('description')
            destination.location = data.get('location')
            db.session.commit()
            return jsonify({'message': 'Destination updated successfully'})
        return jsonify({'message': 'Destination not found'}, 404)

    def delete(self, destination_id):
        destination = Destination.query.get(destination_id)
        if destination is not None:
            db.session.delete(destination)
            db.session.commit()
            return jsonify({'message': 'Destination deleted successfully'})
        return jsonify({'message': 'Destination not found'}, 404)

class ExpenseResource(Resource):
    def post(self):
        data = request.json
        destination_id = data['destination_id']
        expense = Expense(destination_id=destination_id, category=data['category'], amount=data['amount'])
        db.session.add(expense)
        db.session.commit()
        return jsonify({'message': 'Expense added successfully'})

    def get(self, destination_id):
        expenses = Expense.query.filter_by(destination_id=destination_id).all()
        expense_list = []
        for expense in expenses:
            expense_dict = {
                'id': expense.id,
                'category': expense.category,
                'amount': expense.amount
            }
            expense_list.append(expense_dict)
        return jsonify(expense_list)

    def put(self, expense_id):
        expense = Expense.query.get(expense_id)
        if expense is not None:
            data = request.json
            expense.category = data['category']
            expense.amount = data['amount']
            db.session.commit()
            return jsonify({'message': 'Expense updated successfully'})
        return jsonify({'message': 'Expense not found'}, 404)

    def delete(self, expense_id):
        expense = Expense.query.get(expense_id)
        if expense is not None:
            db.session.delete(expense)
            db.session.commit()
            return jsonify({'message': 'Expense deleted successfully'})
        return jsonify({'message': 'Expense not found'}, 404)

class ItineraryResource(Resource):
    def post(self):
        data = request.json
        destination_id = data['destination_id']
        itinerary = Itinerary(destination_id=destination_id, activity=data['activity'])
        db.session.add(itinerary)
        db.session.commit()
        return jsonify({'message': 'Itinerary activity added successfully'})

    def get(self, destination_id):
        itineraries = Itinerary.query.filter_by(destination_id=destination_id).all()
        itinerary_list = []
        for itinerary in itineraries:
            itinerary_dict = {
                'id': itinerary.id,
                'activity': itinerary.activity
            }
            itinerary_list.append(itinerary_dict)
        return jsonify(itinerary_list)

    def put(self, itinerary_id):
        itinerary = Itinerary.query.get(itinerary_id)
        if itinerary is not None:
            data = request.json
            itinerary.activity = data['activity']
            db.session.commit()
            return jsonify({'message': 'Itinerary activity updated successfully'})
        return jsonify({'message': 'Itinerary activity not found'}, 404)

    def delete(self, itinerary_id):
        itinerary = Itinerary.query.get(itinerary_id)
        if itinerary is not None:
            db.session.delete(itinerary)
            db.session.commit()
            return jsonify({'message': 'Itinerary activity deleted successfully'})
        return jsonify({'message': 'Itinerary activity not found'}, 404)

# Add resources to the API
api.add_resource(HelloWorld, '/')
api.add_resource(DestinationResource, '/destinations')
api.add_resource(DestinationDetailResource, '/destinations/<int:destination_id>')
api.add_resource(ExpenseResource, '/expenses')
api.add_resource(ItineraryResource, '/itineraries')

if __name__ == '__main__':
    app.run(debug=True)
