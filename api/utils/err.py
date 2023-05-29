def showError(videoURL, errURL, err):
	print(f'An Error Occured in "{errURL}" url:\n', err)
	if videoURL == 'noURL':
		title = 'No URL Provided'
	else:
		title = 'Error'
		if errURL == '/download':
			errURL = 'downloading'
		elif errURL == '/get_video':
			errURL = 'getting information of'
	return render_template('err.html',
                            title=title,
                            websiteTitle=websiteTitle,
                            errURL=errURL,
                            videoURL=videoURL)