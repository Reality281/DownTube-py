from flask import Blueprint

staticBP = Blueprint('static', __name__)

@staticBP.route('/favicon.ico/')# Route for favicon display of the website
def favicon():
	return render_template('favicon.html', websiteTitle=websiteTitle)# Rendering favicon.html
