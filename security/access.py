from functools import wraps

from flask import redirect, session

from db.user import is_accepted_user


def has_access(user):
    if user is None or 'sub' not in user:
        return False
    
    return is_accepted_user(user['sub'])


def require_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = session.get('user')
        if user is None:
            return redirect("/login")
        if not has_access(user):
            return redirect("/pending-user")
        
        return f(*args, **kwargs)
    return decorated
