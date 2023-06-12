from flask import Blueprint, render_template, request
import pytube
from ..utils.videoFuncs import getVideoID, getVideoLink

apiBP = Blueprint('api', __name__)

@apiBP.route('/<name>/')# Route to api that says hello to the user
def sayHello(name):
    return f'Hello {name}!'

@apiBP.route('/')
def indexTest():
    return render_template('indexTest.html')

@apiBP.route('/get_video_info/')
def get_video_info():
    video_url = request.args.get('video_url')
    try:
        video = pytube.YouTube(video_url)
        title = video.title
        description = video.description
        return render_template('videoInfoTest.html', title=title, description=description)
    except Exception as e:
        return str(e)