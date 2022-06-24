from flask import render_template, Blueprint
from ..models import login_required

home = Blueprint('home', __name__)

@home.route('/')
@login_required
def index():
    """Display overview of user's monthly expenses"""

    return render_template('layout.html')
