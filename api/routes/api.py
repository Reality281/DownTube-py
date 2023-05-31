from flask import Blueprint

BPObj = Blueprint('api', __name__)

@BPObj.route('/<name>')# Route to api that says hello to the user
def sayHello(name):
    return f'Hello {name}!'