from flask import Flask, render_template, request, send_file, redirect, url_for
from pytube import YouTube
from datetime import datetime, timedelta
import os
from .utils.convertors import convertTime, convertViews
from .utils.videoFuncs import getVideoID, getVideoLink
from .utils.err import showError

app = Flask(__name__, template_folder='html', static_folder='public')
websiteTitle = 'DownTube'


@app.errorhandler(404)
def error404(err):
	return render_template('404.html', websiteTitle=websiteTitle)


@app.errorhandler(500)
def error500(err):
	return render_template('500.html', websiteTitle=websiteTitle)


@app.route('/<name>')
def helloName(name):
	return f'Hello {name}!'

@app.route('/')
def index():
	return render_template('index.html', websiteTitle=websiteTitle)


@app.route('/favicon.ico/')
def favicon():
	return render_template('favicon.html', websiteTitle=websiteTitle)


@app.route('/video/', methods=['POST'])
def redirectToVideoInfoPage():
	if request.form['video_url']:
		videoID = getVideoID(request.form['video_url'])
		return redirect(url_for('getVideoInfo', videoID=videoID))
	else:
		showError(videoURL='noURL', errURL='/get_video', err='No URL Provided')


@app.route('/video/<videoID>/')
def getVideoInfo(videoID):
	YTVideoURL = getVideoLink(videoID)
	try:
		yt = YouTube(YTVideoURL)
		views = yt.views
		length = yt.length
		return render_template(
		                        'videoInfo.html',
				                yt=yt,
		                        views=convertViews(views),
		                        length=convertTime(length),
		                        websiteTitle=websiteTitle,
		                        videoID=yt.video_id,
		                        YTVideoURL=YTVideoURL,
		                        videoStreams=yt.streams.filter(progressive=True).order_by('resolution'),
		                        audioStreams=yt.streams.filter(only_audio=True))
	except Exception as e:
		return showError(videoURL=YTVideoURL, errURL='/get_video', err=e)


@app.route('/download/', methods=['POST'])
def redirectToVideoDownloadPage():
	if request.form['video_url']:
		videoID = getVideoID(request.form['video_url'])
	else:
		return showError(videoURL='noURL', errURL='/download', err='No URL Provided')
	if request.form['stream']:
		streamITag = request.form['stream']
	else:
		return showError(videoURL=getVideoLink(videoID), errURL='/download', err='No Stream Provided')
	return redirect(url_for('download', videoID=videoID, streamITag=streamITag))


@app.route('/download/<videoID>/<streamITag>/')
def download(videoID, streamITag):
	YTVideoURL = getVideoLink(videoID)
	try:
		yt = YouTube(YTVideoURL)
		stream = yt.streams.get_by_itag(streamITag)
		filename = f'DownTube-{yt.title}.{stream.mime_type.split("/")[-1]}'
		return redirect(stream.url, code=302)
	except Exception as e:
		return showError(videoURL=YTVideoURL, errURL='/download', err=e)

if __name__ == '__main__':
	app,run(host='0.0.0.0')