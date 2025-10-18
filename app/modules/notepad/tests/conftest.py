import sys
import os
import pytest
from app import create_app
from app.modules.notepad import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import db


@pytest.fixture(scope="module")
def test_client():
    """
    Crea la aplicación Flask en modo testing y devuelve su cliente HTTP.
    Configura una base de datos SQLite en memoria para pruebas.
    """
    app = create_app()
    app.testing = True

    # Configurar la base de datos SQLite en memoria
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()

    yield app.test_client()

    # Limpiar la base de datos después de las pruebas
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture(autouse=True)
def reset_tasks():
    """
    Fixture autouse (se ejecuta antes de cada test).
    Restablece el estado inicial de la lista de blocs de notas.
    """
    models.notepads = [
        {'id': 1, 'title': 'First Note', 'body': 'This is the body of the first note.', 'user_id': 1},
        {'id': 2, 'title': 'Second Note', 'body': 'This is the body of the second note.', 'user_id': 1}
    ]