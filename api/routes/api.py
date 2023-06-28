from flask import Blueprint, render_template, request
import pytube
from ..utils.videoFuncs import getVideoID, getVideoLink
from ..utils.err import showError
from ..utils.jsonFuncs import loadData

apiBP = Blueprint('api', __name__)
config = loadData('config.json')
websiteTitle = config['websiteTitle']

@apiBP.route('/<name>/')# Route to api that says hello to the user
def sayHello(name):
    return f'Hello {name}!'

@apiBP.route('/')
def indexTest():
    return render_template('indexTest.html')


"""
@apiBP.route('/get_video_info2/')
def get_video_info():
    video_url = request.args.get('video_url')
    try:
        video = pytube.YouTube(video_url)
        title = video.title
        description = video.description
        return render_template('videoInfo.html', title=title, description=description)
    except Exception as e:
        return str(e)
"""


@apiBP.route('/get_video_info/')# Route to display Information of the Video
def getVideoInfo():
	YTVideoURL = getVideoLink(getVideoID(request.args.get('video_url')))# Getting the yt video link using the id of the video
	try:
		try:
			yt = YouTube(YTVideoURL)# Getting a YouTube object using the yt video link
		except VideoUnavailable:
			pass
		channelName = Channel(yt.channel_url).channel_name
		views = convertViews(yt.views)# Getting the number of views the video has and converting them to more readable format
		length = convertTime(yt.length)# Getting the duration of the video and converting them to more readable format
		return render_template(# Rendering videoInfo.html
		                        'videoInfo.html',
				                yt=yt,
		                        views=views,
		                        length=length,
								channelName=channelName,
		                        websiteTitle=websiteTitle,
		                        videoID=yt.video_id,
		                        YTVideoURL=YTVideoURL,
		                        videoStreams=yt.streams.filter(progressive=True).order_by('resolution'),# Getting streams with both audio and video objects and rearranging them according resolution
		                        audioStreams=yt.streams.filter(only_audio=True))# Getting streams with only audio objects
	except Exception as e:
		#return showError(videoURL=YTVideoURL, errURL='/video', err=e)# Displaying error if any error occurs
		abort(500, f'An error occured while extracting information from `{YTVideoURL}`')
