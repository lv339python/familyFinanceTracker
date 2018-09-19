"""
This module provides function for validations.
"""

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

MAX_LEN_PASSWORD = 16
MIN_LEN_PASSWORD = 3
SET_KEYS_REG_DATA = {"email", "password"}


def is_valid_password(password):
    """validate password

        Args:
            password (str): The first parameter.

        Returns:
            bool: The return value. True is password valid, else False.

        """
    if not isinstance(password, str):
        return False
    if not MIN_LEN_PASSWORD <= len(password) <= MAX_LEN_PASSWORD:
        return False
    return True


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
