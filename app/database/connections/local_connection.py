from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app.database.entities import BaseEntity


class LocalConnection:
    def __init__(self, url: str) -> None:
        self.session: Optional[Session] = None
        self.engine: Engine = create_engine(url)
        self.Session = sessionmaker(self.engine)
        BaseEntity.metadata.create_all(self.engine)
