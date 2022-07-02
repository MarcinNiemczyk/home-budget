from flask import Blueprint, flash, jsonify, request, redirect, render_template, session, url_for
from sqlalchemy import extract
from datetime import date, datetime
from src.models import login_required, CATEGORIES, TRANSACTION_TYPES, YEARS, MONTHS, Transactions, TransactionsSchema
from src import db
import json


transactions = Blueprint('transactions', __name__)

@transactions.route('/transactions', defaults={'year': date.today().year, 'month': date.today().month, 'transaction_type': 'all'})
@transactions.route('/transactions/<int:year>/<int:month>/<transaction_type>', methods=['GET', 'POST'])
@login_required
def transactions_page(year, month, transaction_type):
    """Show user transactions and allow him to modify data."""

    # Prevent user to access wrong page
    if year not in YEARS:
        flash('Invalid year', category='error')
        return redirect(url_for('transactions.transactions_page'))
    if month < 0 or month > 12:
        flash('Invalid month', category='error')
        return redirect(url_for('transactions.transactions_page'))
    if transaction_type not in TRANSACTION_TYPES:
        flash('Invalid transaction type', category='error')
        return redirect(url_for('transactions.transactions_page'))

    # Get search input
    search_text = request.args.get('q')

    # Get logged user transactions data
    transactions = Transactions.query.filter_by(user_id=session['user_id'])

    # Query for applied month
    if not month == 0:
        transactions = transactions.filter(extract('month', Transactions.date)==month)

    # Query for applied year
    if not year == 0:
        transactions = transactions.filter(extract('year', Transactions.date)==year)

    # Handle transaction type
    if not transaction_type == 'all':
        transactions = transactions.filter_by(type=transaction_type)

    # Handle search functionality
    if search_text:
        transactions = transactions.filter(Transactions.name.like((f'%{search_text}%')))

    # Apply selected filters
    transactions = transactions.all()

    # Ensure text is inside input and handle request
    if search_text is not None:
        transactions_schema = TransactionsSchema()
        output = transactions_schema.dump(transactions, many=True)
        return jsonify(output)

    return render_template('transactions/transactions.html', transactions=transactions, months=MONTHS, years=YEARS, 
           transaction_types=TRANSACTION_TYPES, selected_month=month, selected_year=year, selected_type=transaction_type)


@transactions.route('/transactions/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    """Add or modify transactions"""

    if request.method == 'POST':
        # Validate date input
        date_input = request.form.get('date')
        if len(date_input) != 10:
            flash('Incorrect date', category='error')
            return redirect(url_for('transactions.add_transaction'))
        try:
            year = int(date_input[0:4])
            month = int(date_input[5:7])
            day = int(date_input[8:10])
        except (TypeError, ValueError):
            flash('Incorrect date', category='error')
            return redirect(url_for('transactions.add_transaction'))
        if year not in YEARS:
            flash('Incorrect date', category='error')
            return redirect(url_for('transactions.add_transaction'))
        date_output = date(year, month, day)

        # Validate type input
        transaction_type = request.form.get('transaction_type')
        if transaction_type != 'outcome' and transaction_type != 'income':
            flash('Incorrect transaction type', category='error')
            return redirect(url_for('transactions.add_transaction'))

        # Validate name input
        name = request.form.get('name')
        if len(name) < 2:
            flash('Name is too short', category='error')
            return redirect(url_for('transactions.add_transaction'))
        if len(name) > 99:
            flash('Name is too long', category='error')
            return redirect(url_for('transactions.add_transaction'))

        # Validate amount input
        amount = request.form.get('amount')
        try:
            amount = float(amount)
            amount = round(amount)
        except (TypeError, ValueError):
            flash('Incorrect amount', category='error')
            return redirect(url_for('transactions.add_transaction'))
        if amount <= 0 or amount > 9999999:
            flash('Incorrect amount', category='error')
            return redirect(url_for('transactions.add_transaction'))

        # Validate transaction category input
        category = request.form.get('category')
        if transaction_type == 'outcome' and category not in CATEGORIES['outcome']:
            flash('Incorrect category', category='error')
            return redirect(url_for('transactions.add_transaction'))
        if transaction_type == 'income' and category not in CATEGORIES['income']:
            flash('Incorrect category', category='error')
            return redirect(url_for('transactions.add_transaction'))

        # Create new transaction and add it to database
        new_transaction = Transactions(name=name, type=transaction_type, amount=amount, category=category, date=date_output, user_id = session['user_id'])
        db.session.add(new_transaction)
        db.session.commit()
        flash('Transaction added!', category='success')

    today = date.today()

    return render_template('transactions/add-transaction.html', outcomes=CATEGORIES['outcome'], incomes=CATEGORIES['income'], today=today)


@transactions.route('/remove-transaction', methods=['POST'])
@login_required
def remove_transaction():
    """Removes selected transaction"""
    transaction = json.loads(request.data)
    transactionId = transaction['transactionId']
    transaction = Transactions.query.get(transactionId)
    if transaction:
        if transaction.user_id == session['user_id']:
            db.session.delete(transaction)
            db.session.commit()

    return jsonify({})