import os
from app import create_app
from config import DATABASE_URL

# Получение конфигурации базы данных из переменной окружения или использование значения
# по умолчанию


# Создание экземпляра приложения с конфигурацией
app = create_app(
    {
        'DATABASE_URL': DATABASE_URL
    }
)

if __name__ == '__main__':
    app.run(debug=True)
