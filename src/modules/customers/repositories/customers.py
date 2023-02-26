from src.modules.base_repositories import BaseRepo
from src.modules.customers.entities import Customer


class CustomerRepo(BaseRepo[Customer]):
    entity = Customer
