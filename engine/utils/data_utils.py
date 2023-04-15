import enum
import uuid
import datetime
from typing import List, Dict

from engine.common.consts import CommonConsts


class DataUtils:
    @classmethod
    def serialize_object(cls, obj, time_format=CommonConsts.TIME_FORMAT, include=(), exclude=()) -> Dict:
        result = {}
        for field_name in obj.keys():
            value = obj[field_name]
            if include and field_name not in include:
                continue
            if field_name in exclude:
                continue
            result[field_name] = cls.serialize(value=value, time_format=time_format)
        return result

    @classmethod
    def serialize_objects(cls, objs, time_format=CommonConsts.TIME_FORMAT, include=(), exclude=()) -> List[Dict]:
        return [
            cls.serialize_object(obj=obj, time_format=time_format, include=include, exclude=exclude) for obj in objs
        ]

    @classmethod
    def serialize(cls, value, time_format):
        if isinstance(value, (str, int, float)):
            return value
        elif isinstance(value, uuid.UUID):
            return value.__str__()
        elif isinstance(value, datetime.datetime):
            return value.strftime(time_format)
        elif value.__class__.__class__ is enum.EnumMeta:
            return value.value
        # elif isinstance(value, Base):
        #     return cls.record_to_dict(record=value)
        # elif isinstance(value, list):
        #     serialized_result = []
        #     for value_item in value:
        #         serialized_result.append(cls.object_serialize(value=value_item, time_format=time_format))
        #     return serialized_result
        # elif isinstance(value, dict):
        #     for key in value:
        #         value[key] = cls.object_serialize(value=value[key], time_format=time_format)
        #     return value
        else:
            return value
