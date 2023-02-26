from src.modules.customers.messages import CustomerMessage
from src.modules.customers.dtos import AddCustomerDTO
from src.modules.customers.entities import Customer
from src.modules.customers.repositories import CustomerRepo


class CustomerService:
    def __init__(self):
        self.customer_repo = CustomerRepo

    def get_by_id(self, id: int):
        record = self.customer_repo.get_by_id(id=id)
        if record is None:
            raise Exception(CustomerMessage.ID_NOT_EXISTS)
        return record

    def get_by_phone(self, phone: str):
        records = self.customer_repo.get_by_condition(Customer.phone == phone)
        if len(records) == 0:
            raise Exception(CustomerMessage.PHONE_NOT_EXISTS)
        return records[0]

    def add(self, add_customer_dto: AddCustomerDTO):
        records = self.customer_repo.get_by_condition(Customer.phone == add_customer_dto.phone)
        if len(records) > 0:
            raise Exception(CustomerMessage.PHONE_EXISTS)
        new_record = Customer(**add_customer_dto.dict())
        return self.customer_repo.insert(record=new_record)
