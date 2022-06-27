from flask import render_template, Blueprint, session
from sqlalchemy import extract
from datetime import date
from ..models import CATEGORIES, MONTHS, YEARS, PlannedOutcomes, Transactions, login_required

home = Blueprint('home', __name__)

@home.route('/', defaults={'year': date.today().year, 'month': date.today().month}, methods=['GET', 'POST'])
@home.route('/<int:year>/<int:month>', methods=['GET', 'POST'])
@login_required
def index(year, month):
    """Display overview of user's monthly expenses"""

    # Exclude all months selector
    months = MONTHS.copy()
    del months[0]

    outcomes, sum = get_outcomes(year, month)


    return render_template('home/index.html', months=months, years=YEARS[1::], selected_month=month, selected_year=year, outcomes=outcomes, sum=sum)


def get_outcomes(year, month):
    """placeholder"""

    # Initiate output data
    outcomes = []
    sum = {
        'planned': 0,
        'real': 0,
        'difference': 0
    }

    # Handle every single category data individually
    for category in CATEGORIES['outcomes']:
        outcome = {
            'category': category,
            'planned': 0,
            'real': 0,
            'difference': 0
        }
        # Get planned data and store it in dictionary
        planned = PlannedOutcomes.query.filter_by(user_id=session['user_id'], month=month, year=year, category=category).first()
        if planned:
            outcome['planned'] = planned.amount
            sum['planned'] += planned.amount

        # Get transactions data
        transactions = Transactions.query.filter_by(user_id=session['user_id'], category=category, type='outcome').filter(\
                       extract('year', Transactions.date)==year).filter(extract('month', Transactions.date)==month).all()

        # Sum every transaction
        transactions_sum = 0
        if transactions:
            for transaction in transactions:
                transactions_sum += transaction.amount

        # Store transactions sum as real outcomes in dictionary
        outcome['real'] = transactions_sum
        sum['real'] += transactions_sum
    
        # Add difference
        difference = outcome['planned'] - outcome['real']
        outcome['difference'] = difference
        sum['difference'] += difference

        # Add each category dictionary to list
        outcomes.append(outcome)


    return outcomes, sum