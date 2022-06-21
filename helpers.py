from flask import redirect, session
from functools import wraps


CATEGORIES = {
    'outcomes': ['grocery', 'health', 'house', 'personal', 'media', 'savings', 'debts', 'whims', 'transport', 'gifts', 'travels', 'other'],
    'incomes': ['savings', 'salary', 'bonus', 'interest', 'gifts', 'other']
}

MONTHS = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}

YEARS = [2022 + i for i in range(10)]


def login_required(f):
    """Decorate routes to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function
