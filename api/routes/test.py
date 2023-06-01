from flask import Blueprint, render_template, jsonify

testBP = Blueprint('test', __name__)

@testBP.route('/')
def dynamicIndex():
    return render_template('testIndex.html')
