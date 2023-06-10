from flask import Blueprint, render_template
from pytube import YouTube, Channel
from pytube.exceptions import VideoUnavailable
from ..utils.videoFuncs import getVideoID, getVideoLink
from ..utils.jsonFuncs import loadData


config = loadData('config.json')
websiteTitle = config['websiteTitle']


testBP = Blueprint('test', __name__)


@testBP.route('/')
def indexDebug():
	return render_template('indexDebug.html', websiteTitle=websiteTitle)


@testBP.route('/video/<videoID>/')# Route to display Information of the Video
def getVideoInfoDebug(videoID):
	YTVideoURL = getVideoLink(videoID)# Getting the yt video link using the id of the video
	try:
		try:
			yt = YouTube(YTVideoURL)# Getting a YouTube object using the yt video link
		except VideoUnavailable:
			pass
		channelName = Channel(yt.channel_url).channel_name
		views = convertViews(yt.views)# Getting the number of views the video has and converting them to more readable format
		length = convertTime(yt.length)# Getting the duration of the video and converting them to more readable format
		return render_template(# Rendering videoInfo.html
		                        'videoInfoDebug.html',
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
