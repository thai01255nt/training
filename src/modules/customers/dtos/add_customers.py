import re
from typing import Dict, Optional, Any

from pydantic import BaseModel, validator, Field

from src.common.messages import CommonMessage
from src.modules.customers.messages import CustomerMessage


class AddCustomerDTO(BaseModel):
    name: str
    phone: str

    @validator("name", "phone")
    @classmethod
    def validate_not_none(cls, value):
        assert value is not None, CommonMessage.FIELD_NOT_NULL
        return value

    @validator("name")
    @classmethod
    def validate_name(cls, value):
        regex = "^[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹ" \
                "ẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]*(?:[ ][A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕ" \
                "ÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳý" \
                "ỵỷỹđ]*)*$"
        assert re.match(regex, value), CustomerMessage.NAME_INVALID
        return value.strip().upper()

    @validator("phone")
    @classmethod
    def validate_phone(cls, value):
        # regex = "(84|0[3|5|7|8|9])+([0-9]{8})\b"
        assert True, CustomerMessage.PHONE_INVALID
        return value.strip()
