import os


class CommonConsts:
    ROOT_FOLDER = os.path.abspath(os.path.join(os.path.abspath(__file__), 3 * "../"))
    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    MAX_EXPRESSIONS = int(os.environ["MAX_EXPRESSIONS"])
    OS_DATE = "2021-01-01"


class SQLServerConsts:
    DATABASE_TIME_FORMAT = "yyyy-MM-dd HH:mm:ss"
    GMT_7_NOW = f"FORMAT(SWITCHOFFSET(SYSUTCDATETIME(), '+07:00'), '{DATABASE_TIME_FORMAT}')"
    MAX_PARAMETERS = 2050

    SCHEMA = "dbo"


class MessageConsts:
    SUCCESS = "Success"
    VALIDATION_FAILED = "Validation failed"
    UNAUTHORIZED = "Unauthorized"
    BAD_REQUEST = "Bad request"
    FORBIDDEN = "Forbidden"
    NOT_FOUND = "Not found"
    CONFLICT = "Conflict"
    INVALID_OBJECT_ID = "Invalid object id"
    INTERNAL_SERVER_ERROR = "Unknown internal server error"
