from flask import Blueprint

testBP = Blueprint('test', __name__, template_folder='./testHtml')

@testBP.route('/')
def dynamicIndex():
    return render_template('index.html')

@testBP.route('/page1')
def dynamicPage1():
    return render_template('page1.html')

@testBP.route('/page2')
def dynamicPage2():
    return render_template('page2.html')
