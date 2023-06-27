
import re
import sql_functions

import datetime

def is_valid_password(password):
    # Check if the password length is at least 8 characters
    if len(password) < 8:
        print("Password must be at least 8 characters long")
        return False

    # Check if the password contains at least one lowercase letter
    if not re.search("[a-z]", password):
        print("Password must contain at least one lowercase letter")
        return False

    # Check if the password contains at least one uppercase letter
    if not re.search("[A-Z]", password):
        print("Password must contain at least one uppercase letter")
        return False

    # Check if the password contains at least one digit
    if not re.search("[0-9]", password):
        print( "Password must contain at least one digit")
        return False

    # Check if the password contains at least one special character
    if not re.search("[^a-zA-Z0-9]", password):
        print("Password must contain at least one special character")
        return False

    # Password is valid if all checks pass
    return True, "Password is valid"


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    else:
        return False


def get_current_time():
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time


def extract_month(datetime_str):

    if isinstance(datetime_str, str):
        date_format = "%Y-%m-%d %H:%M:%S"
        datetime_str = datetime.datetime.strptime(datetime_str, date_format)

    # get the name of the month in English
    month_name = datetime_str.strftime('%b').upper()
    return month_name


def add_payment_due(last_day, user_):
    if not user_.get_payment().get_payment_due():
        user_.get_payment().set_payment_due(last_day)


def check_if_user_is_connected():
    user_id = sql_functions.get_id_from_connected_user()
    if not user_id:
        print("no users signed in, please sign in")
    return user_id
