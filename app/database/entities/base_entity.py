from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import MappedAsDataclass


class BaseEntity(MappedAsDataclass, DeclarativeBase):
    pass
