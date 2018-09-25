"""
This module provides function for validations.
"""

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from datetime import date
import calendar

from spending.models import SpendingCategories

SET_KEYS_REG_DATA = {"email", "password"}
SET_KEYS_SPEND_LIMIT_DATA = {"year", "month", "value", "spending_category"}


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


def is_valid_spending_limitation(data):
  """Validate data of spending limitation.

          Args:
              data (dict): contain year, month, value and ID of spending category.

          Returns:
              bool: The return value. True is data valid, else False.

          """

  if not isinstance(data['value'], float):
    return False
  if data['month'] == 0 and data['year'] < date.today().year:
    return False
  if data['month']  and \
    date(data['year'], data['month'], (calendar.monthrange(data['year'], data['month']))[1]) < date.today():
    return False
  return True





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
