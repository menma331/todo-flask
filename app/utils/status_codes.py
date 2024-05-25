THERE_IS_NO_SUCH_TASK: dict = {
    'status': 404,
    'message': 'Задачи с таким id нет.'
}

TASK_SUCCESSFULLY_PUBLISHED: dict = {
    'status': 201,
    'message':
        f'Задача успешно добавлена.',
}

INVALID_JSON_FORMAT: dict = {
    'status': 400,
    'error':
        'Неверный формат JSON.'
}

TASK_SUCCESSFULLY_DELETED: dict = {
    'status': 204,
    'message':
        'Задача успешно удалена.'
}
