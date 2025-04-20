"""Test routes and access control in the Flask application."""

import pytest
from flask_login import login_user
from app import create_app, db
from app.models import User


@pytest.fixture(name="test_client")
def client_fixture():
    """Set up a test client with an in-memory SQLite DB and an admin user."""
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False
    })

    ctx = app.app_context()
    ctx.push()

    db.create_all()
    db.session.add(User(username='testadmin', email='testadmin@example.com', type='Admin'))
    db.session.commit()

    client_instance = app.test_client()
    with client_instance.session_transaction() as session:
        session['_user_id'] = '1'

    yield client_instance

    db.session.remove()
    db.drop_all()
    ctx.pop()

def test_dashboard_loads(test_client):
    """Test that the dashboard page loads for a logged-in user."""
    res = test_client.get('/dashboard')
    assert res.status_code == 200
    assert b'Dashboard Overview' in res.data


def test_api_metrics_cpu(test_client):
    """Test API endpoint for CPU metrics returns proper format."""
    response = test_client.get('/api/metrics/cpu?range=1h')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    for _, entries in data.items():
        assert isinstance(entries, list)
        for entry in entries:
            assert 'timestamp' in entry
            assert 'value' in entry


def test_user_cannot_access_admin(test_client):
    """Test that a regular user is blocked from accessing /admin."""
    with test_client.application.app_context():
        user = User(username='regular', email='user@example.com', type='User')
        db.session.add(user)
        db.session.commit()

        @test_client.application.route("/_login_for_test")
        def _login_for_test():
            fresh_user = db.session.merge(user)
            login_user(fresh_user)
            return "logged in"

    test_client.get("/_login_for_test")

    res = test_client.get("/admin/", follow_redirects=True)
    assert b'Admin Panel' not in res.data
