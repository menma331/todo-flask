import pytest
from app import create_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base


@pytest.fixture(scope='function')
def app():
    test_config = {
        'TESTING': True,
        'DATABASE_URL': 'sqlite:///:memory:'  # Используем базу данных в памяти
    }
    app = create_app(test_config)
    with app.app_context():
        yield app


@pytest.fixture(scope='function')
def client(app):
    return app.test_client()


@pytest.fixture(scope='function')
def session(app):
    # Создаем движок SQLAlchemy
    engine = create_engine(app.config['DATABASE_URL'])
    Session = sessionmaker(bind=engine)

    # Создаем таблицы до начала тестов
    Base.metadata.create_all(engine)

    # Создаем сессию
    session = Session()
    yield session

    # Закрываем сессию и удаляем таблицы после тестов
    session.close()
    Base.metadata.drop_all(engine)
