#===========================================================
# Auth Related Functions
#===========================================================

from flask import redirect, session, flash
from functools import wraps


#-----------------------------------------------------------
# A decorator function to check user logged in
# - This is determined by a 'logged_in' value being present
#   in the session
#-----------------------------------------------------------
def login_required(func):
    @wraps(func)
    # Wrap a given function...
    def wrapper(*args, **kwargs):

        # Is the user logged in?
        if session.get('logged_in'):
            # Yes, so run function
            return func(*args, **kwargs)

        # No, so go to home page
        flash("You need to be logged in", "error")
        return redirect("/")

    return wrapper

#-----------------------------------------------------------
# A decorator function to check if user is admin
# - This is determined by a 'is_admin' value being present
#   in the session
#-----------------------------------------------------------
def admin_required(func):
    @wraps(func)
    # Wrap a given function...
    def wrapper(*args, **kwargs):

        # Is the user an admin?
        if session.get('role')=="admin":
            # Yes, so run function
            return func(*args, **kwargs)

        # No, so go to home page
        flash("You do not have required privileges", "error")
        return redirect("/")

    return wrapper

#-----------------------------------------------------------
# A decorator function to check if user is the election officer
# - This is determined by a 'is_officer' value being present
#   in the session
#-----------------------------------------------------------
def officer_required(func):
    @wraps(func)
    # Wrap a given function...
    def wrapper(*args, **kwargs):

        # Is the user an officer?
        if session.get('is_officer')=="officer":
            # Yes, so run function
            return func(*args, **kwargs)

        # No, so go to home page
        flash("You do not have required privileges", "error")
        return redirect("/")

    return wrapper





