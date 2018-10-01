"""
This module provides function for validations.
"""

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

SET_KEYS_REG_DATA = {"email", "password"}
STR_MIN_LENGTH = 0
STR_MAX_LENGTH = None

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


def list_of_int_validator(value):
  """
  Function that provides list validation
  :param value: list or tuple with integer items
  :type value: list or tuple
  :return: `True` if value if valid and `False` if it is not.
  """
  if not isinstance(value, (list, tuple)):
    return False
  if not value:
    return False
  if not all(isinstance(item, int) for item in value):
    return False
  return True
