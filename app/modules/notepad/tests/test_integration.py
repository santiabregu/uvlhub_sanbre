import pytest
from unittest.mock import patch

from app import db
from app.modules.conftest import login, logout
from app.modules.auth.models import User
from app.modules.profile.models import UserProfile
from flask_login import current_user

@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        user_test = User(email='user@example.com', password='test1234')
        db.session.add(user_test)
        db.session.commit()

        profile = UserProfile(user_id=user_test.id, name="Name", surname="Surname")
        db.session.add(profile)
        db.session.commit()

    yield test_client


def test_get_notepad(test_client):
    """
    Test retrieving a specific notepad via GET request.
    """
    with test_client.application.app_context():
        with patch('app.modules.notepad.services.NotepadService.get_or_404') as mock_get_or_404, \
             patch('flask_login.utils._get_user') as mock_get_user:

            mock_notepad = type('Notepad', (object,), {
                'id': 1, 'title': 'Notepad2', 'body': 'This is the body of notepad2.', 'user_id': 1
            })
            mock_get_or_404.return_value = mock_notepad

            mock_profile = type('UserProfile', (object,), {'name': 'Test', 'surname': 'User'})
            mock_user = type('User', (object,), {
                'is_authenticated': True, 'id': 1, 'profile': mock_profile
            })
            mock_get_user.return_value = mock_user

            response = test_client.get(f'/notepad/{mock_notepad.id}')
            assert response.status_code == 200, "The notepad detail page could not be accessed."
            assert b'Notepad2' in response.data, "The notepad title is not present on the page."

def test_edit_notepad(test_client):
    """
    Test editing a notepad via POST request.
    """
    with test_client.application.app_context():
        with patch('app.modules.notepad.models.Notepad.query') as mock_query:
            mock_notepad = type('Notepad', (object,), {'id': 1, 'title': 'Notepad3', 'body': 'This is the body of notepad3.'})
            mock_query.get.return_value = mock_notepad

            response = test_client.post(f'/notepad/edit/{mock_notepad.id}', data={
                'title': 'Notepad3 Edited',
                'body': 'This is the edited body of notepad3.'
            }, follow_redirects=True)
            assert response.status_code == 200, "The notepad could not be edited."

def test_delete_notepad(test_client):
    """
    Test deleting a notepad via POST request.
    """
    with test_client.application.app_context():
        with patch('app.modules.notepad.models.Notepad.query') as mock_query:
            mock_notepad = type('Notepad', (object,), {'id': 1})
            mock_query.get.return_value = mock_notepad

            response = test_client.post(f'/notepad/delete/{mock_notepad.id}', follow_redirects=True)
            assert response.status_code == 200, "The notepad could not be deleted."
