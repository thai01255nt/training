from collections import Iterable
from datetime import datetime
from typing import Union


from src.utils.string_helper import StringHelperUtils


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
