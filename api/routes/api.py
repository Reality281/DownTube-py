from flask import Blueprint

apiBP = Blueprint('api', __name__)

@apiBP.route('/<name>')# Route to api that says hello to the user
def sayHello(name):
    return f'Hello {name}!'