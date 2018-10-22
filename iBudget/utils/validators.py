"""
This module provides function for validations.
"""
from decimal import Decimal
from datetime import date

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

SET_KEYS_REG_DATA = {"email", "password"}
SET_KEYS_SPENDING_REG_DATA = {'category', 'type_of_pay', 'value'}
SET_KEYS_INCOME_REG_DATA = {'inc_category', 'fund_category', 'value'}
SET_KEYS_FUND_GOAL = {'fund', 'value'}

def is_valid_password(password):
    """validate password

        Args:
            password (str): The first parameter.

        Returns:
            bool: The return value. True is password valid, else False.

    """
    try:
        validate_password(password)
        return True
    except ValidationError:
        return False


def is_valid_registration_data(data):
    """validate data.

            Args:
                data (dict): contain email, password

            Returns:
                bool: The return value. True is data valid, else False.

            """
    if not isinstance(data, dict):
        return False
    if not set(data.keys()) == SET_KEYS_REG_DATA:
        return False

    if not is_valid_password(data["password"]):
        return False
    try:
        validate_email(data["email"])
        return True
    except ValidationError:
        return False


def required_keys_validator(data, keys_required, strict=True):
    """
    :param strict: shows the status of strict method of comparing keys
                   in input data with required keys in method.
    :type strict: Bool
    :return: `True` if data is valid and `False` if it is not valid.
    """
    keys = set(data.keys())
    keys_required = set(keys_required)
    if strict:
        return not keys.symmetric_difference(keys_required)

    return not keys_required.difference(keys)


def email_validator(email):
    """
    Function that provides string validation.
    :param email: String with email data
    :type email: str
    :return: `True` if email if valid and `False` if it is not.
    """

    try:
        email = email.lower().strip()
        validate_email(email)
        return True
    except (ValidationError, AttributeError):
        pass


def login_validate(data):
    """
    Function that provides login data validation.
    :type data: dict
    :return: `True` if data is valid and `None` if it is not.
    :rtype: bool
    """

    if not data:
        return False
    if not required_keys_validator(data, ['email', 'password']):
        return False
    if not email_validator(data['email']):
        return False
    return True


def input_spending_registration_validate(data):
    """validate data.
        Args:
            data (dict): contain category, type of pay, sum, comment
        Returns:
            bool: The return value. True is data valid, else False.list([1,2,3])
    """
    if not set(data.keys()).difference(SET_KEYS_SPENDING_REG_DATA):
        return False
    try:
        data['category'] = int(data['category'])
        data['type_of_pay'] = int(data['type_of_pay'])
        data['value'] = Decimal(data['value'])
        data['comment'] = str(data['comment'])
        return True
    except (ValidationError, AttributeError):
        return False

def input_fund_registration_validate(data):
    """validate data.
        Args:
            data (dict): contain fund, value
        Returns:
            bool: The return value. True is data valid, else False.list([1,2,3])
    """
    if not set(data.keys()).difference(SET_KEYS_FUND_GOAL):
        return False
    try:
        data['fund'] = int(data['fund'])
        data['value'] = Decimal(data['value'])
        return True
    except (ValidationError, AttributeError):
        return False

def input_income_registration_validate(data):
    """validate data.
        Args:
            data (dict): contain category, type of pay, sum, comment
        Returns:
            bool: The return value. True is data valid, else False.list([1,2,3])
    """
    if not set(data.keys()).difference(SET_KEYS_INCOME_REG_DATA):
        return False
    try:
        data['inc_category'] = int(data['inc_category'])
        data['fund_category'] = int(data['fund_category'])
        data['value'] = Decimal(data['value'])
        data['comment'] = str(data['comment'])
        return True
    except (ValidationError, AttributeError):
        return False

def date_range_validate(data):
    """
    Function that provides data range validation
    :param data: start_date, finish_date
    :return: Raise validation error when the starting date is greater than the final one
    """
    if data["start_date"] > data["finish_date"]:
        raise ValidationError("Finish time cannot be earlier than start time!")
    return data

def is_valid_data_individual_limit(data):
    """
    Function that provides login data validation.
    :type data: dict
    :return: 'True' if data is valid and 'None' if it is not.
    :rtype: bool
    """
    if set(data.keys()) != {'spending_id', 'month', 'year', 'value'}:
        return False
    try:
        data['spending_id'] = int(data['spending_id'])
        data['month'] = int(data['month'])
        data['year'] = int(data['year'])
        data['value'] = round(float(data['value']), 2)
        return (data['spending_id'] > 0 and
                -1 < data['month'] < 13 and
                data['year'] >= date.today().year and
                data['value'] > 0)

    except (ValidationError, AttributeError):
        return False


def is_valid_data_new_spending(data):
    """
    Function that provides login data validation.
    :type data: dict
    :return: 'True' if data is valid and 'None' if it is not.
    :rtype: bool
    """
    if set(data.keys()) != {'name', 'icon'} or not data['name']:
        return False
    return True
