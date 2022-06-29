from flask import render_template, Blueprint, session
from sqlalchemy import extract
from datetime import date
from ..models import CATEGORIES, MONTHS, YEARS, PlannedOutcomes, PlannedIncomes, Transactions, login_required

home = Blueprint('home', __name__)

@home.route('/', defaults={'year': date.today().year, 'month': date.today().month}, methods=['GET', 'POST'])
@home.route('/<int:year>/<int:month>', methods=['GET', 'POST'])
@login_required
def index(year, month):
    """Display overview of user's monthly expenses"""

    # Exclude all months selector
    months = MONTHS.copy()
    del months[0]

    outcomes, outcomes_sum = get_statement(year, month, 'outcome')
    incomes, incomes_sum = get_statement(year, month, 'income')


    return render_template('home/index.html', months=months, years=YEARS[1::], selected_month=month, selected_year=year, outcomes=outcomes, outcomes_sum=outcomes_sum,
            incomes=incomes, incomes_sum=incomes_sum)


def get_statement(year, month, transaction_type):
    """Get monthly statement of declared type and return list of dictionaries for each category and overall sum dictionary"""

    # Initiate output data
    statements = []
    sum = {
        'planned': 0,
        'real': 0,
        'difference': 0
    }

    # Handle every single category data individually
    for category in CATEGORIES[transaction_type]:
        statement = {
            'category': category,
            'planned': 0,
            'real': 0,
            'difference': 0
        }
        # Handle planned data query for each transaction type
        if transaction_type == 'outcome':
            planned = PlannedOutcomes.query.filter_by(user_id=session['user_id'], month=month, year=year, category=category).first()
        else:
            planned = PlannedIncomes.query.filter_by(user_id=session['user_id'], month=month, year=year, category=category).first()

        # Ensure user has planned expenses
        if planned:
            statement['planned'] = planned.amount
            sum['planned'] += planned.amount

        # Query database for every transaction of selected type
        transactions = Transactions.query.filter_by(user_id=session['user_id'], category=category, type=transaction_type).filter(\
                       extract('year', Transactions.date)==year).filter(extract('month', Transactions.date)==month).all()

        # Sum every transaction
        transactions_sum = 0
        for transaction in transactions:
            transactions_sum += transaction.amount

        # Store transactions sum as real outcomes in dictionary
        statement['real'] = transactions_sum
        sum['real'] += transactions_sum
    
        # Add difference
        if transaction_type == 'income':
            difference = statement['real'] - statement['planned']
        else:
            difference = statement['planned'] - statement['real']
        statement['difference'] = difference
        sum['difference'] += difference

        # Add each category dictionary to list
        statements.append(statement)


    return statements, sum
