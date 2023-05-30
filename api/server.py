# ========== [ Python module imports ] ==========
from flask import Flask, Response, render_template, request, send_file, redirect, url_for
from pytube import YouTube
from datetime import datetime, timedelta
import os, requests

# ========== [ Local Python file imports ] ==========
from .utils.convertors import convertTime, convertViews
from .utils.videoFuncs import getVideoID, getVideoLink
from .utils.err import showError


# ========== [ Variables ] ==========
app = Flask(__name__, template_folder='html', static_folder='public')
websiteTitle = 'DownTube'


# ========== [ HTTP error handlings ] ==========
@app.errorhandler(404)# 404 Error Handling
def error404(err):
	return render_template('404.html', websiteTitle=websiteTitle)# Rendering 404.html


@app.errorhandler(500)# 500 Error Handling
def error500(err):
	return render_template('500.html', websiteTitle=websiteTitle)# Rendering 500.html


# ========== [ Server Routes ] ==========
@app.route('/api/<name>')# Route to api that says hello to the user
def helloName(name):
	return f'Hello {name}!'

@app.route('/')# Route for main page of the website
def index():
	return render_template('index.html', websiteTitle=websiteTitle)# Rendering index.html


@app.route('/favicon.ico/')# Route for favicon display of the website
def favicon():
	return render_template('favicon.html', websiteTitle=websiteTitle)# Rendering favicon.html


@app.route('/ads.txt/')
def adsTxt():
	return send_file('ads.txt')


@app.route('/video/', methods=['POST'])# Route to redirect user to the Video Info page
def redirectToVideoInfoPage():
	if request.form['video_url']:
		videoID = getVideoID(request.form['video_url'])# Getting the yt video id from the url of the video
		return redirect(url_for('getVideoInfo', videoID=videoID))# Redirecting the user to the Video Info page
	else:
		showError(videoURL='noURL', errURL='/video', err='No URL Provided')# Displaying error if no video url is provided


@app.route('/video/<videoID>/')# Route to display Information of the Video
def getVideoInfo(videoID):
	YTVideoURL = getVideoLink(videoID)# Getting the yt video link using the id of the video
	try:
		yt = YouTube(YTVideoURL)# Getting a YouTube object using the yt video link
		views = convertViews(yt.views)# Getting the number of views the video has and converting them to more readable format
		length = convertTime(yt.length)# Getting the duration of the video and converting them to more readable format
		return render_template(# Rendering videoInfo.html
		                        'videoInfo.html',
				                yt=yt,
		                        views=views,
		                        length=length,
		                        websiteTitle=websiteTitle,
		                        videoID=yt.video_id,
		                        YTVideoURL=YTVideoURL,
		                        videoStreams=yt.streams.filter(progressive=True).order_by('resolution'),# Getting streams with both audio and video objects and rearranging them according resolution
		                        audioStreams=yt.streams.filter(only_audio=True))# Getting streams with only audio objects
	except Exception as e:
		return showError(videoURL=YTVideoURL, errURL='/video', err=e)# Displaying error if any error occurs


@app.route('/download/', methods=['POST'])# Route to redirect the user to the download page of the video
def redirectToVideoDownloadPage():
	if request.form['video_url']:
		videoID = getVideoID(request.form['video_url'])# Getting the yt video id from the url of the video
	else:
		return showError(videoURL='noURL', errURL='/download', err='No URL Provided')# Displaying error if no video url is provided
	if request.form['stream']:
		streamITag = request.form['stream']# Getting the stream of the video the user wants to download
	else:
		return showError(videoURL=getVideoLink(videoID), errURL='/download', err='No Stream Provided')# Displaying error if no stream is provided
	return redirect(url_for('download', videoID=videoID, streamITag=streamITag))# Redirecting the user to the download page with the video id and video stream


@app.route('/download/<videoID>/<streamITag>/')# Route to redirect the user to the url to download the yt video
def download(videoID, streamITag):
	YTVideoURL = getVideoLink(videoID)# Getting the video link of the yt video using the id of the video
	try:
		yt = YouTube(YTVideoURL)# Getting a YouTube object using the yt video link
		stream = yt.streams.get_by_itag(streamITag)# Getting the stream of the video the user wants to download
		filename = f'DownTube-{yt.title}.{stream.mime_type.split("/")[-1]}'# Filename of the yt video
		#return redirect(stream.url, code=302)# Redirecting the user to the url to download yt video
		#return send_file(stream.url, mimetype=stream.mime_type, as_attachment=True, download_name=filename)
		"""response = requests.get(stream.url, stream=True)
		if response.status_code == 200:
			headers = {
				'Content-Disposition': f'attachment; filename="{filename}"',
				'Content-Type': f'{stream.mime_type}'
			}
			return Response(response.iter_content(chunk_size=4096), headers=headers)"""
		return render_template('download.html', websiteTitle=websiteTitle, url=stream.url, title=yt.title)
	except Exception as e:
		return showError(videoURL=YTVideoURL, errURL='/download', err=e)# Displaying error if any error occurs


# ========== [ Running Server ] ==========
if __name__ == '__main__':
	app,run(host='0.0.0.0')# Running server on public network to make it accessible to everyone around the globe