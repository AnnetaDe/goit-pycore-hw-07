import re
from datetime import datetime
from functools import wraps

valid_phone_pattern = re.compile(r'^\+?1?\d{10}$')
valid_birthday_pattern = re.compile(r'^\d{2}\.\d{2}\.\d{4}$')


def is_valid_phone(phone):
    cleaned_phone = re.sub(r"\D", "", phone)
    if len(cleaned_phone) != 10:
        return "Phone number should have 10 digits."
    return valid_phone_pattern.match(cleaned_phone) is not None


def is_valid_birthday(birthday):
    return re.match(r"^\d{2}\.\d{2}\.\d{4}$", birthday) is not None


def is_valid_date(date):
    try:
        datetime.strptime(date, "%d.%m.%Y")
        return True
    except ValueError:
        return False

# decorator for validating phone number and birthday date


def validate_phone(func):
    @wraps(func)
    def wrapper(self, phone, *args, **kwargs):
        if not is_valid_phone(phone):
            raise ValueError("Phone number should have 10 digits.")
        return func(self, phone, *args, **kwargs)
    return wrapper


def validate_birthday(func):
    @wraps(func)
    def wrapper(self, birthday, *args, **kwargs):
        if not is_valid_birthday(birthday) or not is_valid_date(birthday):
            raise ValueError(f"Invalid date format. Use DD.MM.YYYY")
        return func(self, birthday, *args, **kwargs)
    return wrapper
