from flask import Blueprint, render_template
from datetime import date
from ..models import CATEGORIES, MONTHS, YEARS, login_required


planning = Blueprint('planning', __name__)

@planning.route('/planning', defaults={'year': date.today().year, 'month': date.today().month})
@planning.route('/planning/<int:year>/<int:month>', methods=['GET', 'POST'])
@login_required
def planning_page(year, month):
    """Show planned expenses and allow user to modify data"""

    # Exclude all months selector
    months = MONTHS.copy()
    del months[0]


    return render_template('planning/planning.html', outcomes=CATEGORIES['outcomes'], incomes=CATEGORIES['incomes'], years=YEARS[1::], 
           months=months, selected_year=year, selected_month=month)