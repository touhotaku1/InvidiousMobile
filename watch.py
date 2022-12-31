# This file contains the routes for video related tasks
import glob
from flask import request, session, render_template, redirect, url_for, Blueprint
import invidioushandler
import urllib
import subprocess
import os.path
import config

# Define watch blueprint
watch = Blueprint('watch', __name__)

# Get folder size
def getFolderSize(folder):
    total = 0
    for entry in os.scandir(folder):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += getFolderSize(entry.path)
    return total

# Video page route
@watch.route('/watch')
def video():
    # Get video ID
    videoID = request.args.get("v")

    videoInfo = invidioushandler.getVideoMetadata(videoID)

    # Check if the video is already on the server in the videos folder. If so, redirect to cached file
    if os.path.exists('static/videos/' + videoInfo['videoId'] + '-mp4v.mp4'):
        return redirect(url_for('static', filename='videos/' + videoInfo['videoId'] + '-mp4v.mp4'))

    # While cached folder size is greater than 10GB, delete oldest file if it is not in use
    while getFolderSize('static/videos') > config.CACHE_SIZE:
        # Get oldest file
        oldestFile = min(glob.iglob('static/videos/*'), key=os.path.getctime)

        # Try to delete oldest file. If the process fails 5 times, stop the process
        for i in range(5):
            try:
                os.remove(oldestFile)
                break
            except:
                pass

    # Download the video to the server
    urllib.request.urlretrieve(videoInfo['videoUrl'], "static/videos/"+videoID+".mp4")

    # Convert downloaded video to 24 fps mp4v encoding using ffmpeg
    subprocess.call(['ffmpeg', '-i', 'static/videos/'+videoID+'.mp4', '-r', '24', '-c:v', 'mpeg4', '-preset', 'fast', '-crf', '5', '-c:a', 'copy', 'static/videos/'+videoID+'-mp4v.mp4'])

    # Delete the original video
    os.remove("static/videos/"+videoID+".mp4")

    # Redirect user to downloaded video
    return redirect(url_for('static', filename='videos/'+videoID+'-mp4v.mp4'))

# Add route for thumbnail
@watch.route('/thumbnail')
def thumbnail():
    # Get video ID
    videoID = request.args.get("v")

    # Get video metadata
    videoInfo = invidioushandler.getVideoMetadata(videoID)

    # Store thumbnail image in a variable
    thumbnail = urllib.request.urlopen(videoInfo['videoThumbnails'][5]['url']).read()

    # Return thumbnail image
    return thumbnail

# Video info page route
@watch.route('/videoinfo')
def videoinfo():
    # Get video ID
    videoID = request.args.get("v")

    # Get video metadata
    videoInfo = invidioushandler.getVideoMetadata(videoID)

    # Return video metadata
    return render_template('videoPage.html', title = videoInfo['title'], video = videoInfo)