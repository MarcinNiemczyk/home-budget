from flask import Blueprint, render_template
from ..models import login_required


planning = Blueprint('planning', __name__)

@planning.route('/planning')
@login_required
def planning_page():
    """Show planned expenses and allow user to modify data"""

    return render_template('planning/planning.html')