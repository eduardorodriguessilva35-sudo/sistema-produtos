
import os

from flask import Flask
from config import Config
from models import db, Categoria


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object(Config)

os.makedirs(
    os.path.join(BASE_DIR, 'instance'),
    exist_ok=True
)

os.makedirs(
    os.path.join(BASE_DIR, 'static', 'uploads'),
    exist_ok=True
)

db.init_app(app)

from routes import *

with app.app_context():
    db.create_all()

    categorias_iniciais = [
        'Eletrônicos',
        'Roupas',
        'Alimentos'
    ]

    for nome in categorias_iniciais:
        existe = Categoria.query.filter_by(nome=nome).first()

        if not existe:
            db.session.add(Categoria(nome=nome))

    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
