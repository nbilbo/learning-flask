from typing import Dict
from typing import List
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.entities import BaseEntity

if TYPE_CHECKING:
    from app.database.entities import PostEntity


class UserEntity(BaseEntity):
    __tablename__ = 'user'

    __table_args__ = (
        CheckConstraint('username > 0', name='username_not_blank'),
        CheckConstraint('password > 0', name='password_not_blank'),
    )

    iduser: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(init=True, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(init=True, nullable=False)
    posts: Mapped[List['PostEntity']] = relationship(default_factory=list, back_populates='user')

    def asdict(self) -> Dict:
        return {
            'iduser': self.iduser,
            'username': self.username,
            'password': self.password,
            'posts': [post.asdict() for post in self.posts],
        }
