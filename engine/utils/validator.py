import re
from collections import Iterable
from datetime import datetime
from typing import Union

from engine.utils.string_helper import StringHelperUtils

PASSWORD_REGEX = re.compile("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,255}$")
EMAIL_REGEX = re.compile(
    """(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\""""
    """(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")"""
    """@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\"""
    """[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:"""
    """(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])"""
    """.{,64}$"""
)
NAME_REGEX = re.compile("""^[A-Za-z]+((\s)?([A-Za-z])+)*$""")


class Validator:
    @staticmethod
    def validate_not_none(value):
        assert value is not None, "Must be an not null value"

    @staticmethod
    def validate_uuid(value):
        assert StringHelperUtils.is_valid_uuid(value), "Must be an UUID string"

    @staticmethod
    def validate_digit_string(value):
        assert StringHelperUtils.is_valid_digit_string(value), "Must be an digit string"

    @staticmethod
    def validate_allowed(allowed_values, value):
        """{'type': 'list'}"""
        if isinstance(value, Iterable) and not isinstance(value, str):
            unallowed = set(value) - set(allowed_values)
            assert not unallowed, "Must be in list [%s]" % ", ".join(allowed_values)
        else:
            assert value in allowed_values, "Must be in list [%s]" % ", ".join(allowed_values)

    @staticmethod
    def validate_not_allowed(not_allowed_values, value):
        """{'type': 'list'}"""
        if isinstance(value, Iterable) and not isinstance(value, str):
            allowed = set(value) - set(not_allowed_values)
            assert len(allowed) >= len(set(value)), "Must not be in list [%s]" % ", ".join(not_allowed_values)
        else:
            assert value not in not_allowed_values, "Must not be in list [%s]" % ", ".join(not_allowed_values)
        return True, None

    @staticmethod
    def validate_datetime(time_format, value, is_transform) -> Union[str, datetime]:
        try:
            transform_value = datetime.strptime(value, time_format)
            if is_transform:
                value = transform_value
        except Exception:
            assert False, f"Must be in {time_format} time format"
        return value

    @staticmethod
    def validate_password(value):
        """
        The regular expression below cheks that a password:
            Has minimum 8 characters in length. Adjust it by modifying {8,}
            At least one uppercase English letter. You can remove this condition by removing (?=.*?[A-Z])
            At least one lowercase English letter.  You can remove this condition by removing (?=.*?[a-z])
            At least one digit. You can remove this condition by removing (?=.*?[0-9])
            At least one special character,  You can remove this condition by removing (?=.*?[#?!@$%^&*-])
        """
        assert PASSWORD_REGEX.match(value), \
            "Must has minimum 8 and maximum 255 in length, 1 uppercase, 1 lowercase, 1 digit, 1 special character"

    @staticmethod
    def validate_email(value):
        """
        RFC 5322 compliant regex
        """
        assert EMAIL_REGEX.match(value), "Must be an email and has maximum 64 in length"

    @staticmethod
    def validate_name(value):
        assert NAME_REGEX.match(value), "Must only has a-z, A-Z, and space characters"
