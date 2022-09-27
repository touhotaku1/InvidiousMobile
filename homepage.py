# This file contains the routes for homepage related tasks
from flask import request, session, render_template, redirect, url_for, Blueprint
import invidioushandler

# Define homepage blueprint
homepage = Blueprint('homepage', __name__)

# Homepage route
@homepage.route('/')
def home():
    # Render homepage template
    return render_template('home.html', title = "MobileStreamViewer")