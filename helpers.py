from flask import redirect, session
from functools import wraps


CATEGORIES = {
    'outcomes': ['grocery', 'health', 'house', 'personal', 'media', 'savings', 'debts', 'whims', 'transport', 'gifts', 'travels', 'other'],
    'incomes': ['savings', 'salary', 'bonus', 'interest', 'gifts', 'other']
}

def login_required(f):
    """Decorate routes to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function
