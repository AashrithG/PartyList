from faker import Faker
import random

fake = Faker()

people = []

def attendees(number:int):
    """This method will generate a list of attendees"""
    people.clear()
    for item in range(0, number):
        first_name = fake.first_name()
        age = random.randint(13, 100)
        is_attending = random.choice([True, False])
        data = {'first_name': first_name, 'age':age, 'is_attending': is_attending}
        people.append(data)
    return people