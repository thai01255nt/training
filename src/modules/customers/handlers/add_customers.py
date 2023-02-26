from typing import Dict

from src.common.messages import CommonMessage
from src.modules.customers.dtos import AddCustomerDTO
from src.modules.customers.entities import Customer
from src.modules.customers.services import CustomerService
from src.utils.data_utils import DataUtils


class AddCustomerHandler:
    def __init__(self, customer_service: CustomerService):
        self.customer_service = customer_service

    def post(self, data: Dict):
        add_customer_dto = AddCustomerDTO(**data)
        # nếu k pass đc điều kiện của dto sẽ raise lỗi
        # (làm thế nào để catch đc lỗi đó và parse về json và thêm đc thông tin cần thiết trước khi trả về cho user)
        record = self.customer_service.add(add_customer_dto=add_customer_dto)
        # parse entity về dạng json trước khi response qua mạng về cho user
        data = DataUtils.object_to_database_dict(entity=Customer, obj=record)
        result = {
            "message": CommonMessage.CREATED,
            "statusCode": 201,
            "data": data
        }
        return 201, result
        # result là pattern cơ bản của data trả về trong backend, 201 là httpCode biểu thị cho việc tạo thành công
