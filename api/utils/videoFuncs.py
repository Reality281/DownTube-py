def getVideoID(url):# Function to get id of the video
	if 'm.youtube.com/' in url:
		url = url.replace('m.youtube.com', 'www.youtube.com')# Converting 'm.youtube.com' url to 'www.youtube.com' url
	if 'youtu.be' in url:
		videoID = url.strip('/').split('/')[-1]# Converting 'youtu.be' url to 'www.youtube.com' url
	elif 'youtube.com/watch?v=' in url:
		videoID = url.strip('/').split('watch?v=')[-1]# Getting video id from the converted url
	elif 'youtube.com/shorts/' in url:
		videoID = url.strip('/').split('?')[0].split('shorts/')[-1]# Getting video id if the video is a yt shorts
	return videoID# Returning the video id


def getVideoLink(videoID):# Function to get the video url from the video id
	videoURL = f'https://www.youtube.com/watch?v={videoID}'# Creating a video url from the video id
	return videoURL# Returning the video url