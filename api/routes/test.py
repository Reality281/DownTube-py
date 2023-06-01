from flask import Blueprint, render_template, jsonify

testBP = Blueprint('test', __name__)

@testBP.route('/')
def dynamicIndex():
    return render_template('testIndex.html')

@testBP.route('/page1')
def dynamicPage1():
    return render_template('testPage1.html')

@testBP.route('/page2')
def dynamicPage2():
    return render_template('testPage2.html')




@testBP.route('/2')
def dynamicIndex2():
    return render_template('testIndex2.html')

@testBP.route('/update', methods=['POST'])
def dynamicUpdate():
    # Process the AJAX request and return updated content
    # You can fetch data from a database or perform other operations here
    data = {'message': 'New content'}
    return jsonify(data)
