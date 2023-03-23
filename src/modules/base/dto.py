import datetime
from typing import TypeVar

from pydantic import BaseModel, Extra

from src.common.consts import CommonConsts

T = TypeVar("T")


class BaseDTO(BaseModel):
    class Config:
        # allow_population_by_field_name = True
        orm_mode = False
        # validate_assignment = True
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True
        extra = Extra.ignore

        # json_encoders = {
        #     # custom output conversion for datetime
        #     datetime: lambda v: v.strftime(CommonConsts.TIME_FORMAT) if v else None,
        #     # uuid.UUID: lambda v: v.__str__() if v else None,
        #     # SecretStr: lambda v: v.get_secret_value() if v else None,
        # }
