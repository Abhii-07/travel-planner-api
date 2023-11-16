# 🌍 Travel Planner API

## Objective ℹ️
The Travel Planner API serves as a backend system for managing destinations, expenses, and itineraries for travel planning applications. This API provides endpoints to handle CRUD (Create, Read, Update, Delete) operations for destinations, expenses, and itineraries.

## Video Explanation 
- Link : https://drive.google.com/file/d/10qVR4Z1HC23jpWYBIR69MxZ9TLj2s9ul/view?usp=sharing

## User Flow 🚶‍♂️🚶‍♀️
1. **Fetching Destinations:** Users can retrieve a list of destinations or get details of a specific destination.
2. **Managing Expenses:** Allows users to add, update, delete expenses related to a destination.
3. **Handling Itineraries:** Enables users to manage activities or itineraries for a particular destination.

## Endpoints 🛣️
- **GET /destinations:** Retrieve all destinations.
- **POST /destinations:** Create a new destination.
- **GET /destinations/{id}:** Get details of a specific destination.
- **PUT /destinations/{id}:** Update details of a specific destination.
- **DELETE /destinations/{id}:** Delete a destination.

- **GET /expenses:** Get all expenses regardless of the destination.
- **GET /expenses/{destination_id}:** Get expenses for a specific destination.
- **POST /expenses/{destination_id}:** Add an expense related to a destination.
- **PUT /expenses/{destination_id}/{expense_id}:** Update an expense.
- **DELETE /expenses/{destination_id}/{expense_id}:** Delete an expense.

- **GET /itineraries/{destination_id}:** Get itineraries for a specific destination.
- **POST /itineraries/{destination_id}:** Add an itinerary related to a destination.
- **PUT /itineraries/{destination_id}/{itinerary_id}:** Update an itinerary.
- **DELETE /itineraries/{destination_id}/{itinerary_id}:** Delete an itinerary.

## Setup & Usage 🛠️
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
4. Run the application: `flask run`

## Dependencies 📦
- Flask
- Flask-RESTful
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-CORS

## Contributing 🤝
Contributions are welcome! Feel free to open issues or pull requests.

