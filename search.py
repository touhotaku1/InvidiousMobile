# This file contains the routes for search related tasks
from operator import ne
from pydoc import pager
from flask import request, session, render_template, redirect, url_for, Blueprint
import invidioushandler

# Define search blueprint
search = Blueprint('search', __name__)

# Results route with query
@search.route('/results')
def results():
    # Get search query and type
    query = request.args.get("q")
    searchType = "All"
    pageNumber = None

    # If no page number is specified or less than 1, set to 1
    if pageNumber is None or int(pageNumber) <= 0:
        pageNumber = 1

    # If no query is specified, show empty results page
    if query is "" or query is None:
        return render_template('searchPage.html', title = "Search", videos = {})

    # Get search results
    searchResults = invidioushandler.getResults(query, pageNumber, searchType)
    return render_template('searchPage.html', title = query, videos = searchResults)

# Results route for related
@search.route('/related')
def related():
    # Get video ID
    videoID = request.args.get("v")

    # Get related videos
    relatedVideos = invidioushandler.getRelatedVideos(videoID)

    return render_template('searchPage.html', title = "Related Videos", videos = relatedVideos)