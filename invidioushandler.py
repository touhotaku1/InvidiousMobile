import random
from turtle import pos
from webbrowser import get
import config
import requests, json
import urllib.parse
import datetime
from flask import url_for

invidious = config.INVIDIOUS_INSTANCE

def getFeatured():
    featuredURL = invidious+"/api/v1/popular"

    r = requests.get(featuredURL).json()

    for video in r:
        # Store video run time as HH:MM:SS and reformat view count
        video['runTime'] = convertToHMS(video['lengthSeconds'])
        video['viewCount'] = f"{video['viewCount']:,}"

    return r

def getTrendingVideos(category):
    trendingURL = invidious+"/api/v1/trending?type="+category

    r = requests.get(trendingURL).json()

    for video in r:
        # Store video run time as HH:MM:SS, reformat view count, and display category
        video['runTime'] = convertToHMS(video['lengthSeconds'])        
        video['viewCount'] = f"{video['viewCount']:,}"
        video['displayCategory'] = category

    return r

# Gets metadata of a video, as well as adds some parameters
def getVideoMetadata(videoId):
    videoURL = invidious+"/api/v1/videos/"+videoId 

    r = requests.get(videoURL).json()

    # Store possible streams (h.264, 360p and lower, mp4)
    possibleStreams = []

    # Find h264 mp4s in 360p or lower
    for stream in r['formatStreams']:
        if 'container' and 'encoding' and 'resolution' in stream:
            if stream['encoding'] == 'h264' and stream['resolution'] <= '360p' and stream['container'] == 'mp4':
                possibleStreams.append(stream)

    # Sort possible streams (highest resolution first)
    possibleStreams.sort(key=lambda x: x['resolution'], reverse=True)

    # Set videoUrl
    r['videoUrl'] = possibleStreams[0]['url']

    # Get author thumbnail
    r['authorThumbnail'] = r['authorThumbnails'][1]['url']

    # Get percent encoded thumbnail url
    r['percentEncodedThumbnailUrl'] = percentEncode(r['videoThumbnails'][2]['url'])

    # Get percent encoded video url
    r['percentEncodedVideoUrl'] = percentEncode(r['videoUrl'])

    # Format view count
    r['viewCount'] = f"{r['viewCount']:,}"

    # Format ratings
    r['likeCount'] = f"{r['likeCount']:,}"

    # Add upload date
    r['uploadDate'] = convertDate(r['published'])

    # Check if number of tags is greater than 6
    if len(r['keywords']) > 6:
        # Set number of tags to 6
        r['keywords'] = r['keywords'][:6]
    
    return r

# Get comments for a video
def getComments(videoId):
    commentsURL = invidious+"/api/v1/comments/"+videoId

    r = requests.get(commentsURL).json()

    # If there are no comments, return a comment stating such
    if 'comments' in r:
        return r['comments']
    else:
        return [{'author': 'No Comments', 'content': 'There are no comments for this video.',
        'authorThumbnails': url_for('static', filename='icon.png')}]

# Get search results
def getResults(query, pageNumber, searchType):
    if searchType == "User":
        resultsURL = invidious+"/api/v1/search?q="+query+"&type=channel&page="+str(pageNumber)
    else:
        resultsURL = invidious+"/api/v1/search?q="+query+"&type=video&page="+str(pageNumber)

    # These requests occsionally fail, so try again if they do
    try:
        r = requests.get(resultsURL).json()
    except:
        print("Request Failed")
        print(r)
        getResults(query, pageNumber, searchType)

    # Format runTime and viewCount
    for video in r:
        # Store video run time as HH:MM:SS and reformat view count
        video['runTime'] = convertToHMS(video['lengthSeconds'])
        video['viewCount'] = f"{video['viewCount']:,}"

    return r

# Converts time in seconds to HH:MM:SS
def convertToHMS(timeInSeconds):
    if(timeInSeconds // 60) >= 60:
        # For videos 1 hour or longer, convert to HH:MM:SS
        hours = timeInSeconds // 60 // 60
        minutes = (timeInSeconds - (hours * 60 * 60)) // 60
        seconds = timeInSeconds % 60
        return str(hours) + ':' + str(minutes).zfill(2) + ':' + str(seconds).zfill(2)
    else:
        return str(timeInSeconds // 60) + ':' + str(timeInSeconds % 60).zfill(2)

# Gets related videos
def getRelatedVideos(videoId):
    # Get video metadata
    videoURL = invidious+"/api/v1/videos/"+videoId

    videoMetadata = requests.get(videoURL).json()

    # Return related videos
    return videoMetadata['recommendedVideos']

# Converts URL to percent encoded URL
def percentEncode(url):
    return urllib.parse.quote(url, safe='')

# Convert date from epoch time to Month DD, YYYY
def convertDate(date):
    convertedDate = datetime.datetime.fromtimestamp(date)
    return convertedDate.strftime('%B %d, %Y')