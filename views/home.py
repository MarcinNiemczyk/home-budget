from decimal import DivisionByZero
from flask import flash, redirect, render_template, Blueprint, request, session, url_for
from sqlalchemy import extract
from datetime import date
from ..models import CATEGORIES, MONTHS, YEARS, PlannedOutcomes, PlannedIncomes, StartingBalance, Transactions, login_required
from .. import db

home = Blueprint('home', __name__)

@home.route('/', defaults={'year': date.today().year, 'month': date.today().month}, methods=['GET', 'POST'])
@home.route('/<int:year>/<int:month>', methods=['GET', 'POST'])
@login_required
def index(year, month):
    """Display overview of user's monthly expenses"""

    # Exclude all months selector
    months = MONTHS.copy()
    del months[0]

    # Get statements and overall sum of every category
    outcomes, outcomes_sum = get_statement(year, month, 'outcome')
    incomes, incomes_sum = get_statement(year, month, 'income')

    # Get length of outcomes/incomes charts
    outcomes_chart_length = calculate_chart_length(outcomes_sum['planned'], outcomes_sum['real'])
    incomes_chart_length = calculate_chart_length(incomes_sum['planned'], incomes_sum['real'])

    # Get user's starting balance
    starting_balance = StartingBalance.query.filter_by(user_id=session['user_id'], month=month, year=year).first()

    # Update starting balance
    if request.method == 'POST':
        updated_amount = request.form.get('starting-balance')
        # Validate input
        try:
            updated_amount = int(updated_amount)
        except ValueError:
            flash('Incorrect amount', category='error')
            return redirect(url_for('home.index', year=year, month=month))
        if updated_amount < 0 or updated_amount > 9999999:
            flash('Incorrect amount', category='error')
            return redirect(url_for('home.index', year=year, month=month))
        
        # Update database
        new_starting_balance = StartingBalance(amount=updated_amount, month=month, year=year, user_id=session['user_id'])
        if starting_balance:
            starting_balance.amount = updated_amount
        else:
            db.session.add(new_starting_balance)
        db.session.commit()

        flash('Starting balance updated!', category='success')
        return redirect(url_for('home.index', year=year, month=month))

    # Assign int value (amount) to starting balance
    if starting_balance:
        starting_balance = starting_balance.amount
    else:
        starting_balance = 0

    # Final and starting balance chart
    final_balance = starting_balance - outcomes_sum['real'] + incomes_sum['real']
    balance_chart_length = calculate_chart_length(starting_balance, final_balance)
    
    # Overall statistics of current month
    try:
        savings_increase = int(((final_balance / starting_balance) - 1) * 100)
    except ZeroDivisionError:
        savings_increase = final_balance
    saved = final_balance - starting_balance

    return render_template('home/index.html', months=months, years=YEARS[1::], selected_month=month, selected_year=year, outcomes=outcomes, outcomes_sum=outcomes_sum,
            incomes=incomes, incomes_sum=incomes_sum, outcomes_chart_length=outcomes_chart_length, incomes_chart_length=incomes_chart_length, starting_balance=starting_balance,
            final_balance=final_balance, balance_chart_length=balance_chart_length, savings_increase=savings_increase, saved=saved)


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


def calculate_chart_length(n1, n2):
    """Return length values for charts"""
    
    # Handle negative final balance
    if n2 < 0:
        chart_length = [100, 0]
    # Handle minus and zero values
    elif n1 == 0 and n2 == 0:
        chart_length = [100, 100]
    elif n1 == 0:
        if n2 > 0:
            chart_length = [0, 100]
        else:
            chart_length = [100, 0]
    elif n2 == 0:
        if n1 > 0:
            chart_length = [100, 0]
        else:
            chart_length = [0, 100]
    # Calculate ratio
    else:
        if n1 > n2:
            chart_length = [100, round((n2 / n1) * 100)]
        else:
            chart_length = [round((n1 / n2) * 100), 100]

    return chart_length