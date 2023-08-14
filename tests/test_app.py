import pytest
from main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get('/')
    assert b'Notes' in response.data


def test_create_note(client):
    response = client.post('/create', data={'content': 'Test note'})
    assert response.status_code == 302  # Перенаправление после создания
    assert b'Test note' in client.get('/').data


def test_view_note(client):
    client.post('/create', data={'content': 'Test note'})
    response = client.get('/note/1')
    assert b'Test note' in response.data


def test_delete_note(client):
    client.post('/create', data={'content': 'Delete note'})
    response = client.post('/delete/1', follow_redirects=True)
    assert b'Delete note' not in response.data
