from datetime import datetime

from sqlalchemy import Integer, String, DateTime, Text
from sqlalchemy.dialects.mysql import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Базовый класс модели."""
    pass


class Task(Base):
    """
    Модель Задачи(обращаться к `task`).

    Атрибуты:
        * `id`: (ForeignKey): уникальный индекс задачи.
        * `title`: (str): заголовок задачи.
        * `description`: (int): описание задачи.
        * `created_at`: (DateTime): время создания задачи.
        * `updated_at`: (DateTime): время обновления задачи.
    """

    __tablename__ = 'task'
    id: Mapped[int] = mapped_column(type_=Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(type_=String(45), nullable=False)
    description: Mapped[str] = mapped_column(type_=Text, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        type_=TIMESTAMP, default=datetime.utcnow
    )
    updated_at: Mapped[DateTime] = mapped_column(
        type_=TIMESTAMP, default=datetime.utcnow
    )

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
