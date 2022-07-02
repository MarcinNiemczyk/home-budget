from flask import Blueprint, flash, render_template, redirect, url_for, session, request
from datetime import date
from src import db
from src.models import CATEGORIES, MONTHS, YEARS, PlannedIncomes, PlannedOutcomes, login_required


planning = Blueprint('planning', __name__)

@planning.route('/planning', defaults={'year': date.today().year, 'month': date.today().month}, methods=['GET', 'POST'])
@planning.route('/planning/<int:year>/<int:month>', methods=['GET', 'POST'])
@login_required
def planning_page(year, month):
    """Show planned expenses and allow user to modify data"""

    # Prevent user to access wrong page
    if year not in YEARS[1::]:
        flash('Invalid year', category='error')
        return redirect(url_for('planning.planning_page'))
    if month < 1 or month > 12:
        flash('Invalid month', category='error')
        return redirect(url_for('planning.planning_page'))

    # Exclude all months selector
    months = MONTHS.copy()
    del months[0]

    # Get user all planned outcomes and incomes 
    planned_outcomes = PlannedOutcomes.query.filter_by(user_id=session['user_id'])
    planned_incomes = PlannedIncomes.query.filter_by(user_id=session['user_id'])

    # Apply year filter
    planned_outcomes = planned_outcomes.filter_by(year=year)
    planned_incomes = planned_incomes.filter_by(year=year)

    # Apply month filter
    planned_outcomes = planned_outcomes.filter_by(month=month).all()
    planned_incomes = planned_incomes.filter_by(month=month).all()

    if request.method == 'POST':
        # Handle request for planned outcomes
        if request.form.get('save_button') == 'Update Outcomes':
            # Validate every category input
            for category in CATEGORIES['outcome']:
                # Ensure amount is integer
                try:
                    amount = int(request.form.get(category))
                except ValueError:
                    flash('Amount must be a number value', category='error')
                    return redirect(url_for('planning.planning_page', year=year, month=month))
                # Ensure amount is correct value
                if amount < 0 or amount > 9999999:
                    flash('Incorrect amount', category='error')
                    return redirect(url_for('planning.planning_page', year=year, month=month))
                
                # Add category to database
                new_record = PlannedOutcomes(category=category, amount=amount, month=month, year=year, user_id=session['user_id'])
                if planned_outcomes:
                    for record in planned_outcomes:
                        if record.category == category:
                            record.amount = amount
                else:
                    db.session.add(new_record)
            
            # Update database
            db.session.commit()
            flash('Planned outcomes updated!', category='success')

            return redirect(url_for('planning.planning_page', year=year, month=month))
        
        # Handle request for planned incomes
        elif request.form.get('save_button') == 'Update Incomes':
            # Validate every category input
            for category in CATEGORIES['income']:
                # Ensure amount is integer
                try:
                    amount = int(request.form.get(category))
                except ValueError:
                    flash('Amount must be a number value', category='error')
                    return redirect(url_for('planning.planning_page', year=year, month=month))
                # Ensure amount is correct value
                if amount < 0 or amount > 9999999:
                    flash('Incorrect amount', category='error')
                    return redirect(url_for('planning.planning_page', year=year, month=month))
                
                # Add category to database
                new_record = PlannedIncomes(category=category, amount=amount, month=month, year=year, user_id=session['user_id'])
                if planned_incomes:
                    for record in planned_incomes:
                        if record.category == category:
                            record.amount = amount
                else:
                    db.session.add(new_record)
            
            # Update database
            db.session.commit()
            flash('Planned incomes updated!', category='success')

            return redirect(url_for('planning.planning_page', year=year, month=month))
        
    return render_template('planning/planning.html', outcomes=CATEGORIES['outcome'], incomes=CATEGORIES['income'], years=YEARS[1::], 
           months=months, selected_year=year, selected_month=month, planned_outcomes=planned_outcomes, planned_incomes=planned_incomes)
