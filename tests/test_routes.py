import pytest
from app import create_app, db
from app.models import User
from flask_login import login_user

@pytest.fixture
def client():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False
    })

    with app.app_context():
        db.create_all()
        db.session.add(User(username='testadmin', email='testadmin@example.com', type='Admin'))
        db.session.commit()

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['_user_id'] = '1' 
        yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()

def test_dashboard_loads(client):
    res = client.get('/dashboard')
    assert res.status_code == 200
    assert b'Dashboard Overview' in res.data

def test_api_metrics_cpu(client):
    response = client.get('/api/metrics/cpu?range=1h')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    for machine, entries in data.items():
        assert isinstance(entries, list)
        for entry in entries:
            assert 'timestamp' in entry
            assert 'value' in entry

def test_user_cannot_access_admin(client):
    with client.application.app_context():
        user = User(username='regular', email='user@example.com', type='User')
        db.session.add(user)
        db.session.commit()

        @client.application.route("/_login_for_test")
        def _login_for_test():
            fresh_user = db.session.merge(user)
            login_user(fresh_user)
            return "logged in"

    client.get("/_login_for_test")

    res = client.get("/admin/", follow_redirects=True)
    assert b'Admin Panel' not in res.data
