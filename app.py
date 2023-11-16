from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
import os
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/wanderlust_backend_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://wanderlust_db_nrjl_user:VmGCV1UCo6iqaSM3AowE5U4TqTCufYC9@dpg-clat58bmot1c7385bl0g-a.singapore-postgres.render.com/wanderlust_db_nrjl'
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
            # Delete associated expenses first
            associated_expenses = Expense.query.filter_by(destination_id=destination_id).all()
            for expense in associated_expenses:
                db.session.delete(expense)
            db.session.commit()

            # Now delete the destination
            db.session.delete(destination)
            db.session.commit()
            return jsonify({'message': 'Destination deleted successfully'})
        return jsonify({'message': 'Destination not found'}, 404)

class ExpenseResource(Resource):
    def get(self, destination_id=None):
        try:
            if destination_id:
                expenses = Expense.query.filter_by(destination_id=destination_id).all()
                if not expenses:
                    return jsonify({'message': 'No expenses found for the destination'}), 404

                expense_list = []
                for expense in expenses:
                    expense_dict = {
                        'id': expense.id,
                        'category': expense.category,
                        'amount': expense.amount
                    }
                    expense_list.append(expense_dict)

                return jsonify(expense_list)
            else:
                expenses = Expense.query.all()
                if not expenses:
                    return jsonify({'message': 'No expenses found'}), 404

                expense_list = []
                for expense in expenses:
                    expense_dict = {
                        'id': expense.id,
                        'destination_id': expense.destination_id,
                        'category': expense.category,
                        'amount': expense.amount
                    }
                    expense_list.append(expense_dict)

                return jsonify(expense_list)
        except Exception as e:
            return jsonify({'message': f'Error in retrieving expenses: {str(e)}'}), 500

    def post(self, destination_id):
        try:
            data = request.json
            if not Destination.query.get(destination_id):
                return jsonify({'message': 'Destination not found for the expense'}), 404

            expense = Expense(destination_id=destination_id, category=data['category'], amount=data['amount'])
            db.session.add(expense)
            db.session.commit()
            return jsonify({'message': 'Expense added successfully'})
        except KeyError:
            return jsonify({'message': 'Invalid request data. Please provide all required fields.'}), 400
        except Exception as e:
            return jsonify({'message': f'Error in creating expense: {str(e)}'}), 500


class ExpenseDetailResource(Resource):
    def put(self, destination_id, expense_id):
        try:
            expense = Expense.query.get(expense_id)
            if expense:
                data = request.json
                expense.category = data['category']
                expense.amount = data['amount']
                db.session.commit()
                return jsonify({'message': 'Expense updated successfully'})
            return jsonify({'message': 'Expense not found'}), 404
        except KeyError:
            return jsonify({'message': 'Invalid request data. Please provide all required fields.'}), 400
        except Exception as e:
            return jsonify({'message': f'Error in updating expense: {str(e)}'}), 500

    def delete(self, destination_id, expense_id):
        try:
            expense = Expense.query.get(expense_id)
            if expense:
                db.session.delete(expense)
                db.session.commit()
                return jsonify({'message': 'Expense deleted successfully'})
            return jsonify({'message': 'Expense not found'}), 404
        except Exception as e:
            return jsonify({'message': f'Error in deleting expense: {str(e)}'}), 500



class ItineraryListResource(Resource):
    def get(self, destination_id):
        try:
            itineraries = Itinerary.query.filter_by(destination_id=destination_id).all()
            if not itineraries:
                return jsonify({'message': 'No itineraries found for the destination'}), 404

            itinerary_list = []
            for itinerary in itineraries:
                itinerary_dict = {
                    'id': itinerary.id,
                    'activity': itinerary.activity
                }
                itinerary_list.append(itinerary_dict)

            return jsonify(itinerary_list)
        except Exception as e:
            return jsonify({'message': f'Error in retrieving itineraries: {str(e)}'}), 500

    def post(self, destination_id):
        try:
            data = request.json
            if not Destination.query.get(destination_id):
                return jsonify({'message': 'Destination not found for the itinerary'}), 404

            itinerary = Itinerary(destination_id=destination_id, activity=data['activity'])
            db.session.add(itinerary)
            db.session.commit()
            return jsonify({'message': 'Itinerary activity added successfully'})
        except KeyError:
            return jsonify({'message': 'Invalid request data. Please provide all required fields.'}), 400
        except Exception as e:
            return jsonify({'message': f'Error in creating itinerary: {str(e)}'}), 500


class ItineraryDetailResource(Resource):
    def put(self, destination_id, itinerary_id):
        try:
            itinerary = Itinerary.query.get(itinerary_id)
            if itinerary:
                data = request.json
                itinerary.activity = data['activity']
                db.session.commit()
                return jsonify({'message': 'Itinerary activity updated successfully'})
            return jsonify({'message': 'Itinerary activity not found'}), 404
        except KeyError:
            return jsonify({'message': 'Invalid request data. Please provide all required fields.'}), 400
        except Exception as e:
            return jsonify({'message': f'Error in updating itinerary activity: {str(e)}'}), 500

    def delete(self, destination_id, itinerary_id):
        try:
            itinerary = Itinerary.query.get(itinerary_id)
            if itinerary:
                db.session.delete(itinerary)
                db.session.commit()
                return jsonify({'message': 'Itinerary activity deleted successfully'})
            return jsonify({'message': 'Itinerary activity not found'}), 404
        except Exception as e:
            return jsonify({'message': f'Error in deleting itinerary activity: {str(e)}'}), 500

# Updated endpoints
api.add_resource(HelloWorld, '/')
api.add_resource(DestinationResource, '/destinations')
api.add_resource(DestinationDetailResource, '/destinations/<int:destination_id>')
api.add_resource(ExpenseResource, '/expenses', '/expenses/<int:destination_id>')
api.add_resource(ExpenseDetailResource, '/expenses/<int:destination_id>/<int:expense_id>')
api.add_resource(ItineraryListResource, '/itineraries/<int:destination_id>')
api.add_resource(ItineraryDetailResource, '/itineraries/<int:destination_id>/<int:itinerary_id>')


# if __name__ == '__main__':
#     app.run(debug=True)
