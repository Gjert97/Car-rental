# routes.py
from flask import request, jsonify, Flask
from model import Car, Customer, Employee
from db import Neo4jDB

app = Flask(__name__)


@app.route('/')
def index():
    return "Car Rental API"

# Initialize the Neo4j database connection
db = Neo4jDB(uri="neo4j+s://fb45896d.databases.neo4j.io", user="neo4j", password="5UceHwbCnsrcdfst6RajeRP-oqQMZY850Y-c_aVcvi4")

# CREATE a new car
@app.route('/cars', methods=['POST'])
def create_car():
    data = request.json
    car_id = data['car_id']
    make = data['make']
    model = data['model']
    year = data['year']
    location = data['location']
    
    # Create car in Neo4j
    db.create_car(car_id, make, model, year, location, 'available')
    
    return jsonify({"message": "Car added successfully!", "car_id": car_id}), 201

# READ all cars
@app.route('/cars', methods=['GET'])
def get_cars():
    cars = db.get_all_cars()  # Get cars from Neo4j
    return jsonify(cars), 200

# UPDATE a car by ID
@app.route('/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    car = db.get_car_by_id(car_id)  # Get car from Neo4j
    if not car:
        return jsonify({"message": "Car not found"}), 404
    
    data = request.json
    db.update_car(car_id, data.get('make'), data.get('model'), data.get('year'), data.get('location'), data.get('status'))
    
    return jsonify({"message": "Car updated successfully"}), 200

# DELETE a car by ID
@app.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    car = db.get_car_by_id(car_id)  # Get car from Neo4j
    if not car:
        return jsonify({"message": "Car not found"}), 404
    
    db.delete_car(car_id)
    return jsonify({"message": "Car deleted successfully"}), 200

# CREATE customer
@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.json
    customer_id = data['customer_id']
    name = data['name']
    age = data['age']
    address = data['address']
    
    # Create customer in Neo4j
    db.create_customer(customer_id, name, age, address)
    
    return jsonify({"message": "Customer added successfully!", "customer_id": customer_id}), 201

# READ all customers
@app.route('/customers', methods=['GET'])
def get_customers():
    customers = db.get_all_customers()  # Get customers from Neo4j
    return jsonify(customers), 200

# UPDATE customer by ID
@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = db.get_customer_by_id(customer_id)  # Get customer from Neo4j
    if not customer:
        return jsonify({"message": "Customer not found"}), 404
    
    data = request.json
    db.update_customer(customer_id, data.get('name'), data.get('age'), data.get('address'))
    
    return jsonify({"message": "Customer updated successfully"}), 200

# DELETE customer by ID
@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = db.get_customer_by_id(customer_id)  # Get customer from Neo4j
    if not customer:
        return jsonify({"message": "Customer not found"}), 404
    
    db.delete_customer(customer_id)
    return jsonify({"message": "Customer deleted successfully"}), 200

# Order car (book)
@app.route('/order-car', methods=['POST'])
def order_car():
    data = request.json
    customer_id = data['customer_id']
    car_id = data['car_id']
    
    customer = db.get_customer_by_id(customer_id)
    car = db.get_car_by_id(car_id)
    
    if not customer:
        return jsonify({"message": "Customer not found"}), 404
    if not car or car['status'] != 'available':
        return jsonify({"message": "Car not available"}), 400
    
    # Ensure customer hasn't booked another car
    if db.customer_has_booked_car(customer_id):
        return jsonify({"message": "Customer already has a car booked"}), 400
    
    # Book the car
    db.update_car_status(car_id, 'booked')
    return jsonify({"message": f"Car {car_id} booked for customer {customer_id}"}), 200

# Cancel car booking
@app.route('/cancel-order-car', methods=['POST'])
def cancel_order_car():
    data = request.json
    customer_id = data['customer_id']
    car_id = data['car_id']
    
    car = db.get_car_by_id(car_id)
    if not car or car['status'] != 'booked':
        return jsonify({"message": "Car not booked"}), 400
    
    # Make car available
    db.update_car_status(car_id, 'available')
    return jsonify({"message": f"Car {car_id} is now available"}), 200

# Rent car
@app.route('/rent_car', methods=['POST'])
def rent_car():
    data = request.json
    customer_id = data['customer_id']
    car_id = data['car_id']
    
    car = db.get_car_by_id(car_id)
    if not car or car['status'] != 'booked':
        return jsonify({"message": "Car is not booked"}), 400
    
    # Rent the car
    db.update_car_status(car_id, 'rented')
    return jsonify({"message": f"Car {car_id} is now rented by customer {customer_id}"}), 200

# Return car
@app.route('/return-car', methods=['POST'])
def return_car():
    data = request.json
    customer_id = data['customer_id']
    car_id = data['car_id']
    car_status = data.get('status', 'available')  # Can be 'available' or 'damaged'
   
    car = db.get_car_by_id(car_id)
    if not car or car['status'] != 'rented':
        return jsonify({"message": "Car is not rented"}), 400
    
    # Return the car and update status
    db.update_car_status(car_id, car_status)
    return jsonify({"message": f"Car {car_id} returned by customer {customer_id} and status set to {car_status}"}), 200


if __name__ == '__main__':
    app.run(debug=True)