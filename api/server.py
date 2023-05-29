from flask import Flask, render_template, request, send_file, redirect, url_for
from pytube import YouTube
from datetime import datetime, timedelta
import os

app = Flask(__name__, template_folder='html', static_folder='public')
websiteTitle = 'DownTube'

def convertTime(sec):
	time = ''
	dur = {
		'Years': 365 * 24 * 3600,
		'Days': 24 * 3600,
		'Hours': 3600,
		'Minutes': 60
    }
	for d in dur.keys():
		if int(sec) // dur[d]:
			time += f"{sec//dur[d]} {d} "
			sec %= dur[d]
	if sec:
		time += f"{sec} Seconds"
	return time

def convertViews(view):
	views = {'Crore': 10000000, 'Lakh': 100000, 'Thousand': 1000}
	for v in views.keys():
		if isinstance(view, int):
			if view // views[v]:
				view = f"{round(view/views[v], 1)} {v}"
	return view


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


def getVideoLink2(url):
	videoURL = ''
	if 'm.youtube.com/' in url:
		url = url.replace('m.youtube.com', 'www.youtube.com')
	if 'youtu.be' in url:
		videoID = url.strip('/').split('/')[-1]
		videoURL = f'https://www.youtube.com/watch?v={videoID}'
	elif 'youtube.com/watch?v=' in url:
		videoURL = url.strip('/')
	elif 'youtube.com/shorts/' in url:
		videoURL = url.strip('/').split('?')[0]
	return videoURL


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


def delOldVids():
	folder = './public/vids/'
	currentTime = datetime.now()
	oneHourAgo = currentTime - timedelta(hours=1)
	for file in os.listdir(folder):
		filePath = os.path.join(folder, file)
		if os.path.isfile(filePath):
			creationTime = datetime.fromtimestamp(os.path.getctime(filePath))
			if creationTime < oneHourAgo:
				os.remove(filePath)
				print(f'Deleted {filePath}')


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