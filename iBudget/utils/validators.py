"""
This module provides function for validations.
"""
from decimal import Decimal, DecimalException
from datetime import date

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.dateparse import parse_date

SET_KEYS_REG_DATA = {"email", "password", "confirm_password"}
SET_KEYS_SPENDING_REG_DATA = {'category', 'type_of_pay', 'value'}
SET_KEYS_CREATE_FUND_DATA = {'name', 'icon'}
SET_KEYS_INCOME_REG_DATA = {'inc_category', 'fund_category', 'value'}
SET_KEYS_FUND_CREATE_DATA = {'name', 'icon'}
SET_KEYS_FUND_GOAL = {'value', 'name', 'icon'}
SET_KEYS_GROUP_CREATE_DATA = {'name', 'icon'}
KEYS_SET_ADD_USER_TO_GROUP = {'users_email', 'group_id', 'is_admin'}
STR_MIN_LENGTH = 0
STR_MAX_LENGTH = None


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
    except ValidationError as err:
        print(err)
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
        data['name'] = str(data['name'])
        data['icon'] = str(data['icon'])
        data['value'] = Decimal(data['value'])
        return True
    except (ValueError, AttributeError):
        return False

def input_income_registration_validate(data):
    """
    validate data.
    Args:
        data (dict): contains   income category, fund category, value, comment
    Returns:
        bool: The return value. True is data valid, else False
    """
    if not set(data.keys()).difference(SET_KEYS_INCOME_REG_DATA):
        return False
    try:
        data['inc_category'] = int(data['inc_category'])
        data['fund_category'] = int(data['fund_category'])
        data['value'] = Decimal(data['value'])
        data['comment'] = str(data['comment'])
        return True
    except (ValidationError, AttributeError, TypeError, DecimalException):
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
    Function that provides data validation for defining new limitation.
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


def string_validator(value, min_length=STR_MIN_LENGTH, max_length=STR_MAX_LENGTH):
    """
    Function that provides string validation.
    :param value: the string literal itself.
    :type value: string
    :param min_length: the minimal length of the received string value.
    :type min_length: integer
    :param max_length: the maximum length of the received string value.
    :type max_length: integer
    :return: `True` if value if valid and `False` if it is not.
    """

    if not isinstance(value, str):
        return False

    if len(value) < min_length:
        return False

    if max_length:
        if len(value) > max_length:
            return False

    return True


def updating_password_validate(data, new_password):
    """
    :param data: dict that we need to validate.
    :type data: dict
    :param new_password: new_password for required_keys_validator
    :type new_password: str
    :return: `True` if data is valid and `None` if it is not.
    """

    if data:
        if not required_keys_validator(data, [new_password], False):
            return False
        string = data.get(new_password)
        if not string_validator(string, 4):
            return False
        if is_valid_password(string):
            return True
    return False


def updating_email_validate(data, email):
    """
    :param data: dict that we need to validate.
    :type data: dict
    :param email: email for required_keys_validator
    :type email: str
    :return: `True` if data is valid and `None` if it is not.
    """
    if data:
        if not required_keys_validator(data, [email], False):
            return False
        if not string_validator(data.get(email), 4):
            return False
        if email_validator(data.get(email)):
            return True
    return False


def is_valid_data_new_spending(data):
    """
    Function that provides data validation for creating new spending category.
    :type data: dict
    :return: 'True' if data is valid and 'None' if it is not.
    :rtype: bool
    """
    if set(data.keys()) != {'name', 'icon'} or not data['name']:
        return False
    return True


def is_valid_data_spending_history(data):
    """
    Function that provides data validation for creating spending history.
    :type data: dict
    :return: 'True' if data is valid and 'None' if it is not.
    :rtype: bool
    """
    if set(data.keys()) != {'start_date', 'finish_date', 'UTC'}:
        return False
    try:
        parse_date(data['start_date'])
        parse_date(data['finish_date'])
        int(data['UTC'])
        if data['start_date'] <= data['finish_date']:
            return True
        return False

    except (ValidationError, AttributeError):
        return False


def is_valid_data_create_new_group(data):
    """validate data.
        Args:
            data (dict): contain name and icon
        Returns:
            bool: The return value. True is data valid, else False.
    """
    if set(data.keys()) != SET_KEYS_GROUP_CREATE_DATA:
        return False
    if not data['name']:
        return False
    try:
        data['name'] = str(data['name'])
        return True
    except(ValueError, AttributeError):
        return False


def is_valid_data_create_new_fund(data):
    """validate data.
        Args:
            data (dict): contain name and icon
        Returns:
            bool: The return value. True is data valid, else False.
    """
    if not set(data.keys()).difference(SET_KEYS_FUND_CREATE_DATA):
        return False
    try:
        data['name'] = str(data['name'])
        data['icon'] = str(data['icon'])
        return True
    except(ValueError, AttributeError):
        return False


def is_valid_data_new_income(data):
    """
    Function that provides income creation validation
    :param data:
    :return:
    """
    if set(data.keys()) != {'name', 'icon', 'date', 'value'} or not data['name']:
        return False
    if not is_valid_date(data['date']):
        return False
    return True


def is_valid_date(date_to_validate):
    """
    Function that provides date validation
    :param string
    :return: True if date is date
    """
    try:
        parse_date(date_to_validate)
    except ValueError:
        return False
    return True


def is_valid_data_add_user_to_group(data):
    """validate data.
        Args:
            data (dict): contain email, group id and user id
        Returns:
            bool: The return value. True is data valid, else False.
    """
    if set(data.keys()) != KEYS_SET_ADD_USER_TO_GROUP:
        return False
    try:
        data['group_id'] = int(data['group_id'])
        data['is_admin'] = bool(data['is_admin'])
        validate_email(data['users_email'])
    except(ValueError, AttributeError):
        return False
    return True
