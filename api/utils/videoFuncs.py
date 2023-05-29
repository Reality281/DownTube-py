def getVideoID(url):
	if 'm.youtube.com/' in url:
		url = url.replace('m.youtube.com', 'www.youtube.com')
	if 'youtu.be' in url:
		videoID = url.strip('/').split('/')[-1]
	elif 'youtube.com/watch?v=' in url:
		videoID = url.strip('/').split('watch?v=')[-1]
	elif 'youtube.com/shorts/' in url:
		videoID = url.strip('/').split('?')[0].split('shorts/')[-1]
	return videoID


def getVideoLink(videoID):
	videoURL = f'https://www.youtube.com/watch?v={videoID}'
	return videoURL