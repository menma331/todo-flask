from pydantic import BaseModel, Field


class TaskAddUpdateSchema(BaseModel):
    """
    Схема для добавления задачи.

    Атрибуты:
        * `title` (str): заголовок задачи.
        * `description` (str): описание задачи.
    """
    title: str = Field(
        min_length=1, max_length=100, example="Купить автомобиль",
        description='Краткое описание задачи'
    )
    description: str = Field(
        min_length=1, max_length=500,
        example="Нужно купить автомобиль. Сейчас выбираю между Mazda и Volkswagen.",
        description='Подробное описание задачи'
    )


class GetTaskByIdSchema(BaseModel):
    """
    Схема для получения задачи по id.

    Атрибуты:
        * `id` (int): id задачи.
    """
    id: int = Field(title="id", description="Id задачи", example=1)
