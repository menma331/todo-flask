from app.utils.status_codes import TASK_SUCCESSFULLY_DELETED


def test_add_task(client):
    """
    Тест кейс получения всех задач.

    GET запрос на адрес 127.0.0.1:5000/tasks
    """
    # Отправляем POST запрос для добавления задачи
    response = client.post(
        '/tasks', json={"title": "Task 1", "description": "Description 1"}
    )

    # Проверяем, что ответ сервера имеет код 200 OK
    assert response.status_code == 200

    # Проверяем, что в ответе есть ожидаемые данные
    assert 'id' in response.json
    assert 'title' in response.json
    assert 'description' in response.json
    assert 'created_at' in response.json
    assert 'updated_at' in response.json


def test_get_task_by_id(client):
    """
    Тест кейс получения задачи по id.

    GET запрос на адрес 127.0.0.1:5000/tasks/{id}
    """
    # Предварительно добавляем задачу
    client.post('/tasks', json={"title": "Task 1", "description": "Description 1"})

    # Отправляем GET запрос для получения задачи по id
    response = client.get('/tasks/1')

    # Проверяем, что ответ сервера имеет код 200 OK
    assert response.status_code == 200

    # Проверяем, что в ответе есть ожидаемые данные
    assert 'id' in response.json
    assert 'title' in response.json
    assert 'description' in response.json
    assert 'created_at' in response.json
    assert 'updated_at' in response.json


def test_update_task_by_id(client):
    """
    Тест кейс обновления задачи по id.

    PUT запрос на адрес 127.0.0.1:5000/tasks/{id}
    """
    # Предварительно добавляем задачу
    client.post('/tasks', json={"title": "Task 1", "description": "Description 1"})

    # Отправляем PUT запрос для обновления задачи по id
    response = client.put(
        '/tasks/1', json={
            "title": "Updated Task 1", "description": "Updated Description 1"
        }
    )

    # Проверяем, что ответ сервера имеет код 200 OK
    assert response.status_code == 200

    # Проверяем, что в ответе есть ожидаемые данные
    assert 'id' in response.json
    assert response.json['title'] == "Updated Task 1"
    assert response.json['description'] == "Updated Description 1"


def test_delete_task_by_id(client):
    """
    Тест кейс удаления задачи по id.

    DELETE запрос на адрес 127.0.0.1:5000/tasks/{id}
    """
    # Предварительно добавляем задачу
    client.post('/tasks', json={"title": "Task 1", "description": "Description 1"})

    # Отправляем DELETE запрос для удаления задачи по id
    response = client.delete('/tasks/1')

    # Проверяем, что ответ сервера имеет код 200 OK
    assert response.status_code == 200

    # Проверяем, что задача успешно удалена
    assert response.json == TASK_SUCCESSFULLY_DELETED
