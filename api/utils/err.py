def showError(videoURL, errURL, err):# Function to display errors
	from flask import render_template
	from ..utils.jsonFuncs import loadData

	config = loadData('config.json')
	websiteTitle = config['websiteTitle']

	print(f'An Error Occured in "{errURL}" url:\n', err)# Printing the error to the console
	if videoURL == 'noURL':# Checking if the error is due to no url of the yt video
		title = 'No URL Provided'
	else:# If the error is not due to no url of the yt video
		title = 'Error'
		if errURL == '/download':# Checking if the error occured in '/download' route
			errURL = 'downloading'
		elif errURL == '/video':# Checking if the error occured in the '/video' route
			errURL = 'getting information of'
	return render_template('err.html',# Rendering err.html
                            title=title,
                            websiteTitle=websiteTitle,
                            errURL=errURL,
                            videoURL=videoURL)