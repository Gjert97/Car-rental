from neo4j import GraphDatabase

from neo4j import GraphDatabase


class Neo4jDB:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    # Create a new car in the database
    def create_car(self, car_id, make, model, year, location, status):
        with self.driver.session() as session:
            session.run(
                "CREATE (c:Car {car_id: $car_id, make: $make, model: $model, year: $year, location: $location, status: $status})",
                car_id=car_id, make=make, model=model, year=year, location=location, status=status
            )

    # Get all cars from the database
    def get_all_cars(self):
        with self.driver.session() as session:
            result = session.run("MATCH (c:Car) RETURN c")
            cars = []
            for record in result:
                car = record["c"]
                cars.append({
                    "car_id": car["car_id"],
                    "make": car["make"],
                    "model": car["model"],
                    "year": car["year"],
                    "location": car["location"],
                    "status": car["status"]
                })
            return cars

    # Get a car by ID
    def get_car_by_id(self, car_id):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (c:Car {car_id: $car_id}) RETURN c", car_id=car_id
            )
            record = result.single()
            return record["c"] if record else None

    # Update a car's details
    def update_car(self, car_id, make, model, year, location, status):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (c:Car {car_id: $car_id})
                SET c.make = $make, c.model = $model, c.year = $year, c.location = $location, c.status = $status
                """,
                car_id=car_id, make=make, model=model, year=year, location=location, status=status
            )

    # Delete a car by ID
    def delete_car(self, car_id):
        with self.driver.session() as session:
            session.run("MATCH (c:Car {car_id: $car_id}) DETACH DELETE c", car_id=car_id)

    # Create a new customer
    def create_customer(self, customer_id, name, age, address):
        with self.driver.session() as session:
            session.run(
                "CREATE (c:Customer {customer_id: $customer_id, name: $name, age: $age, address: $address})",
                customer_id=customer_id, name=name, age=age, address=address
            )

    # Get all customers from the database
    def get_all_customers(self):
        with self.driver.session() as session:
            result = session.run("MATCH (c:Customer) RETURN c")
            customers = []
            for record in result:
                customer = record["c"]
                customers.append({
                    "customer_id": customer["customer_id"],
                    "name": customer["name"],
                    "age": customer["age"],
                    "address": customer["address"]
                })
            return customers

    # Get a customer by ID
    def get_customer_by_id(self, customer_id):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (c:Customer {customer_id: $customer_id}) RETURN c", customer_id=customer_id
            )
            record = result.single()
            return record["c"] if record else None

    # Update a customer's details
    def update_customer(self, customer_id, name, age, address):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (c:Customer {customer_id: $customer_id})
                SET c.name = $name, c.age = $age, c.address = $address
                """,
                customer_id=customer_id, name=name, age=age, address=address
            )

    # Delete a customer by ID
    def delete_customer(self, customer_id):
        with self.driver.session() as session:
            session.run(
                "MATCH (c:Customer {customer_id: $customer_id}) DETACH DELETE c",
                customer_id=customer_id
            )

    # Check if a customer has booked another car
    def customer_has_booked_car(self, customer_id):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (c:Car {status: 'booked'})-[:BOOKED_BY]->(cust:Customer {customer_id: $customer_id})
                RETURN c
                """,
                customer_id=customer_id
            )
            return result.single() is not None

    # Update a car's status
    def update_car_status(self, car_id, status):
        with self.driver.session() as session:
            session.run(
                "MATCH (c:Car {car_id: $car_id}) SET c.status = $status",
                car_id=car_id, status=status
            )

    # Book a car (create a relationship between customer and car)
    def book_car_for_customer(self, customer_id, car_id):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (c:Car {car_id: $car_id}), (cust:Customer {customer_id: $customer_id})
                CREATE (c)-[:BOOKED_BY]->(cust)
                SET c.status = 'booked'
                """,
                customer_id=customer_id, car_id=car_id
            )

    # Rent a car (change status from 'booked' to 'rented')
    def rent_car(self, car_id):
        with self.driver.session() as session:
            session.run(
                "MATCH (c:Car {car_id: $car_id}) SET c.status = 'rented'",
                car_id=car_id
            )

    # Return a car and update its status
    def return_car(self, car_id, status):
        with self.driver.session() as session:
            session.run(
                "MATCH (c:Car {car_id: $car_id}) SET c.status = $status",
                car_id=car_id, status=status
            )

    # Cancel a car booking
    def cancel_car_booking(self, car_id):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (c:Car {car_id: $car_id})-[r:BOOKED_BY]->()
                DELETE r
                SET c.status = 'available'
                """,
                car_id=car_id
            )
