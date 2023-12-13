from datetime import datetime

from typing import Dict
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.entities import BaseEntity

if TYPE_CHECKING:
    from app.database.entities import UserEntity


class PostEntity(BaseEntity):
    __tablename__ = 'post'

    __table_args__ = (
        CheckConstraint('title > 0', name='title_not_blank'),
        CheckConstraint('body > 0', name='body_not_blank'),
    )

    idpost: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str] = mapped_column(init=True, nullable=False)
    body: Mapped[str] = mapped_column(init=True, nullable=False)
    created: Mapped[datetime] = mapped_column(init=False, default=datetime.now())

    user: Mapped['UserEntity'] = relationship(init=True)
    id_user: Mapped[int] = mapped_column(ForeignKey('user.iduser'), init=False)

    def asdict(self) -> Dict:
        return {
            'idpost': self.idpost,
            'title': self.title,
            'body': self.body,
            'created': self.created,
            'id_user': self.id_user,
            'username': self.user.username,
        }
