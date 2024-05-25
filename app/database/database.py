from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.models.models import Task, Base


class DBConnection:
    """
    Класс для работы с базой данных (MySQL).
    """

    def __init__(self, database_url, test=False):
        self.engine = create_engine(url=database_url)
        session = sessionmaker(bind=self.engine, class_=Session)
        self.__session = session()

        if test:
            self.create_all_tables()

    def create_all_tables(self):
        """
        Метод для создания всех таблиц в базе данных.
        """
        Base.metadata.create_all(self.engine)

    def get_all_tasks(self):
        """
        Метод для получения списка всех существующих задач.
        """
        tasks = self.__session.query(Task).all()
        task_list = [task.as_dict() for task in tasks]
        return task_list

    def add_task(self, task_data: dict) -> Task:
        """
        Метод для добавления новой задачи.
        """
        new_task = Task(
            title=task_data.get('title'),
            description=task_data.get('description')
        )
        self.__session.add(new_task)
        self.__session.commit()
        return new_task

    def get_task_by_id(self, task_id: int) -> Task | bool:
        """Метод для получения задачи по определенному id.

        Аргументы:
            * `task_id` (int): id задачи.
        """
        task = self.__session.query(Task).filter(Task.id == task_id).first()
        if task:
            return task
        else:
            return False

    def update_task_by_id(self, task_id, task_data) -> Task | bool:
        """
        Метод для обновления задачи по id.

        Аргументы:
            * `task_id` (int): id задачи.
        """
        task = self.__session.query(Task).filter(Task.id == task_id).first()
        if task:
            task.title = task_data.get('title')
            task.description = task_data.get('description')
            task.updated_at = datetime.utcnow()
            self.__session.commit()
            return task
        else:
            return False

    def delete_task_by_id(self, id) -> bool:
        """
        Метод для удаления задачи по id.

        Аргументы:
            * `id` (int): id задачи.
        """
        task = self.__session.query(Task).filter(Task.id == id).first()
        if task:
            self.__session.delete(task)
            self.__session.commit()
            return True
        else:
            return False

    def close_connection(self) -> None:
        """
        Метод для закрытия соединения с базой данных.
        """
        self.__session.close()
