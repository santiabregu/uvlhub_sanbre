from app.modules.mycrud.repositories import MycrudRepository
from core.services.BaseService import BaseService


class MycrudService(BaseService):
    def __init__(self):
        super().__init__(MycrudRepository())
