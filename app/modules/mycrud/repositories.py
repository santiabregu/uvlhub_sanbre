from app.modules.mycrud.models import Mycrud
from core.repositories.BaseRepository import BaseRepository


class MycrudRepository(BaseRepository):
    def __init__(self):
        super().__init__(Mycrud)
