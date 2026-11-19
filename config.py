
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get(
        'SECRET_KEY',
        'chave-local-apenas-para-desenvolvimento'
    )

    SQLALCHEMY_DATABASE_URI = (
        'sqlite:///' +
        os.path.join(BASE_DIR, 'instance', 'produtos.db')
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
