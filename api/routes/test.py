from flask import Blueprint, render_template

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
