# This file handles the Flask application

# Import config information
import config
from flask import Flask
# Import homepage blueprint
from homepage import homepage
# Import search blueprint
from search import search
# Import watch blueprint
from watch import watch
# Import featured blueprint
from featured import featured

# Define Flask app
app = Flask(__name__)

# Register the needed blueprints
app.register_blueprint(homepage)
app.register_blueprint(search)
app.register_blueprint(watch)
app.register_blueprint(featured)

# Secret Key (Needed for sessions in Flask)
app.secret_key = config.SECRET_KEY