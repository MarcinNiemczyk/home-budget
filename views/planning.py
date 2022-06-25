from flask import Blueprint, render_template
from ..models import CATEGORIES, MONTHS, YEARS, login_required


planning = Blueprint('planning', __name__)

@planning.route('/planning')
@login_required
def planning_page():
    """Show planned expenses and allow user to modify data"""

    return render_template('planning/planning.html', outcomes=CATEGORIES['outcomes'], incomes=CATEGORIES['incomes'], years=YEARS, months=MONTHS, selected_month=6, selected_year=2022)