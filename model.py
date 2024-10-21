class Car:
    def __init__(self, id, make, model, year, location, status):
        self.id = id
        self.make = make
        self.model = model
        self.year = year
        self.location = location
        self.status = status

class Customer:
    def __init__(self, id, name, age, address):
        self.id = id
        self.name = name
        self.age = age
        self.address = address

class Employee:
    def __init__(self, id, name, address, branch):
        self.id = id
        self.name = name
        self.address = address
        self.branch = branch
