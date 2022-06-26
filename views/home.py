from flask import render_template, Blueprint
from datetime import date
from ..models import MONTHS, YEARS, login_required

home = Blueprint('home', __name__)

@home.route('/', defaults={'year': date.today().year, 'month': date.today().month}, methods=['GET', 'POST'])
@home.route('/<int:year>/<int:month>', methods=['GET', 'POST'])
@login_required
def index(year, month):
    """Display overview of user's monthly expenses"""

    # Exclude all months selector
    months = MONTHS.copy()
    del months[0]

    return render_template('home/index.html', months=months, years=YEARS[1::], selected_month=month, selected_year=year)
