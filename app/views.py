from flasgger import swag_from
from flask import request, jsonify, current_app as app
from app.schema import TaskAddUpdateSchema, GetTaskByIdSchema
from app.utils.status_codes import (
    THERE_IS_NO_SUCH_TASK, INVALID_JSON_FORMAT, TASK_SUCCESSFULLY_DELETED,
)


@app.teardown_appcontext
def shutdown_session(exception=None):
    """
    Метод закрывает базу по завершению работы сервера.
    """
    app.db_connection.close_connection()


@app.route('/tasks', methods=['GET'])
@swag_from(
    {
        'description': 'Эндпоинт для получения списка всех задач.',
        'responses': {
            200: {
                'description': 'Пример ответа',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id': {
                                'type': 'integer',
                                'example': 1
                            },
                            'title': {
                                'type': 'str',
                                'example': 'Напиши письмо !'
                            },
                            'description': {
                                'type': 'str',
                                'example': 'Напиши письмо своему старому другу.'
                            },
                            'created_at': {
                                'type': 'datetime',
                                'example': 'Sat, 25 May 2024 08:00:30 GMT'
                            },
                            'updated_at': {
                                'type': 'datetime',
                                'example': 'Sat, 25 May 2024 08:00:30 GMT'
                            }
                        }
                    }
                }
            }
        }
    }
)
def get_tasks():
    """
    GET метод для получения списка всех существующих задач.
    """
    return jsonify(app.db_connection.get_all_tasks())


@app.route('/tasks', methods=['POST'])
@swag_from(
    {
        'description': 'Эндпоинт для добавления новой задачи.\n\n'
                       'Ожидает JSON в формате: {"title": "Название задачи", '
                       '"description": "Описание задачи"}.',
        'schema': TaskAddUpdateSchema.schema(),
        'parameters': [
            {
                'name': 'Добавление задачи',
                'in': 'body',
                'required': True,
                'schema': TaskAddUpdateSchema.schema()
            },

        ],
        'responses': {
            201: {
                'description': 'Пример ответа',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id': {
                                'type': 'integer',
                                'example': 1
                            },
                            'title': {
                                'type': 'str',
                                'example': 'Купить автомобиль'
                            },
                            'description': {
                                'type': 'str',
                                'example': 'Нужно купить автомобиль. Сейчас выбираю '
                                           'между Mazda и Volkswagen.'
                            },
                            'created_at': {
                                'type': 'datetime',
                                'example': 'Sat, 25 May 2024 08:00:30 GMT'
                            },
                            'updated_at': {
                                'type': 'datetime',
                                'example': 'Sat, 25 May 2024 08:00:30 GMT'
                            }
                        }
                    }
                }
            }
        }
    }
)
def add_task():
    """
    POST метод для добавления задачи в список.
    """
    try:
        task_data = request.json
        title = task_data.get('title')
        description = task_data.get('description')
        if title is None or description is None:
            return jsonify(
                INVALID_JSON_FORMAT
            ), 400

        # Создаем словарь с данными новой задачи
        new_task = {"title": title, "description": description}
        task = app.db_connection.add_task(new_task)  # В случае успеха вернет объект Task

        return jsonify(
            {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'created_at': task.created_at,
                'updated_at': task.updated_at
            }
        ), 201
    except Exception as e:
        app.logger.error(f"Ошибка при добавлении задачи: {e}")
        return jsonify(
            {
                "error": "Внутренняя ошибка сервера",
                "details": str(e)
            }
        ), 500



@app.route('/tasks/<int:id>', methods=['GET'])
@swag_from(
    {
        'description': 'Эндпоинт для получения определенной задачи по id.',
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'format': 'int32',
                'pattern': '^[0-9]*$',
                'schema': GetTaskByIdSchema.schema()
            }
        ],
        'responses': {
            200: {
                'description': 'Пример положительного ответа',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer', 'example': 1},
                        'title': {'type': 'string', 'example': 'Купить автомобиль'},
                        'description': {
                            'type': 'string',
                            'example': 'Нужно купить автомобиль. Сейчас выбираю между '
                                       'Mazda и Volkswagen.'
                        },
                        'created_at': {
                            'type': 'datetime', 'example': 'Sat, 25 May 2024 08:00:30 GMT'
                        },
                        'updated_at': {
                            'type': 'datetime', 'example': 'Sat, 25 May 2024 08:00:30 GMT'
                        }
                    }
                }
            },
            404: {
                'description': 'Пример отрицательного ответа',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'status': {'type': 'integer', 'example': 404},
                        'message': {'type': 'string', 'example': 'Задачи с таким id нет.'}
                    }
                }
            }
        }
    }
)
def get_task_by_id(id: int):
    """
    GET метод для получения задачи по id.
    """
    task = app.db_connection.get_task_by_id(id)
    if task:
        response = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'created_at': task.created_at,
            'updated_at': task.updated_at
        }
        return jsonify(response), 200
    else:
        response = THERE_IS_NO_SUCH_TASK
        return jsonify(response), 404


@app.route('/tasks/<int:id>', methods=['PUT'])
@swag_from(
    {
        'description': 'PUT метод для обновления задачи по id. Ожидает JSON '
                       'в формате: {"title": "Название задачи", '
                       '"description": "Описание задачи"}.',
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'format': 'int32',
                'pattern': '^[0-9]*$',
                'schema': GetTaskByIdSchema.schema()
            },
            {
                'name': 'Обновление задачи',
                'in': 'body',
                'required': True,
                'schema': TaskAddUpdateSchema.schema()
            }
        ],
        'responses': {
            202: {
                'description': 'Пример положительного ответа',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer', 'example': 1},
                        'title': {'type': 'string', 'example': 'Купить автомобиль'},
                        'description': {
                            'type': 'string',
                            'example': 'Нужно купить автомобиль. Сейчас выбираю между '
                                       'Mazda и Volkswagen.'
                        },
                        'created_at': {
                            'type': 'datetime', 'example': 'Sat, 25 May 2024 08:00:30 GMT'
                        },
                        'updated_at': {
                            'type': 'datetime', 'example': 'Sat, 25 May 2024 08:00:30 GMT'
                        }
                    }
                }
            },
            404: {
                'description': 'Пример отрицательного ответа',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'status': {'type': 'integer', 'example': 404},
                        'message': {'type': 'string', 'example': 'Задачи с таким id нет.'}
                    }
                }
            }
        }
    }
)
def update_task_by_id(id: int):
    """
    PUT метод для обновления задачи по id.
    """
    try:
        task_data = request.json
        title = task_data.get('title')
        description = task_data.get('description')
        if title is None or description is None:
            return jsonify(INVALID_JSON_FORMAT), 400

        updated_task = {"title": title, "description": description}
        task = app.db_connection.update_task_by_id(id, updated_task)
        if task:
            response = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'created_at': task.created_at,
                'updated_at': task.updated_at
            }
            return jsonify(response), 202
        else:
            response = THERE_IS_NO_SUCH_TASK
            return jsonify(response), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/tasks/<int:id>', methods=['DELETE'])
@swag_from(
    {
        'description': 'DELETE метод для удаления задачи по id.',
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'required': True,
                'format': 'int32',
                'pattern': '^[0-9]*$',
                'schema': GetTaskByIdSchema.schema()
            }
        ],
        'responses': {
            200: {
                'description': 'Пример положительного ответа',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'status': {'type': 'integer', 'example': 200},
                        'message': {
                            'type': 'string', 'example': 'Задача успешно удалена.'
                        }
                    }
                }
            },
            404: {
                'description': 'Пример отрицательного ответа',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'status': {'type': 'integer', 'example': 404},
                        'message': {'type': 'string', 'example': 'Задачи с таким id нет.'}
                    }
                }
            }
        }
    }
)
def delete_task_by_id(id: int):
    """
    DELETE метод для удаления задачи по id.
    """
    task = app.db_connection.delete_task_by_id(id)
    if task:
        response = TASK_SUCCESSFULLY_DELETED
        return jsonify(response), 200
    else:
        response = THERE_IS_NO_SUCH_TASK
        return jsonify(response), 404
