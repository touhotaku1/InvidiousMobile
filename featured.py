# This file contains the routes for featured page related tasks
from flask import request, session, render_template, redirect, url_for, Blueprint
import invidioushandler

# Define homepage blueprint
featured = Blueprint('featured', __name__)

# featuredPage route
@featured.route('/featuredPage')
def featuredPage():
    # Render homepage template
    return render_template('featured.html', title = "Featured", videos = invidioushandler.getFeatured())