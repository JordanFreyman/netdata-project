# Distributed Systems Monitor

A Flask-based web application for monitoring system metrics across a distributed cluster. This project fetches real-time data using the Netdata API, logs it to a local database, and provides a secure, interactive dashboard for administrators and users.

## Live Deployment

[jordanfreyman.me](https://jordanfreyman.me)

## Features

- Real-time and historical system metric visualizations (CPU, Memory, Disk, Network)
- Google OAuth 2.0 login for secure access
- Role-Based Access Control (Admin vs. User views)
- Admin-only panel powered by Flask-Admin
- SQLite database for persistent metric logs
- Periodic metric logging from Netdata
- Handles and displays unreachable machines
- Dashboard with range-based metric filters (1h, 24h, 7d)

## rchitecture

- **Frontend**: Jinja2 templates + Chart.js for visualizations
- **Backend**: Flask, SQLAlchemy, Flask-Login, Authlib
- **Database**: SQLite (no external server required)
- **Metrics Source**: Netdata API (on cluster machines)
- **Security**: Google OAuth, role checking, access logging

## etup & Installation

### 1. Clone the repo

```bash
git clone https://gitlab.com/cop45219911608/project3.git
cd cop4521-flask
```

### 2. Set up environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Google OAuth

Create a `.env` file or edit your `config.py`:
```bash
GOOGLE_CLIENT_ID="your-client-id"
GOOGLE_CLIENT_SECRET="your-client-secret"
SECRET_KEY="your-flask-secret"
```

### 4. Run the app

```bash
flask run
```

### 5. Run metric logger manually

```bash
python -m app.logger
```

## Running Tests

```bash
pytest tests/
```

If pytest is installed in your virtual environment, be sure to activate it in the root project directory using:
```bash
source venv/bin/activate
```

## Project Structure

```
cop4521-flask/
├── app/
│   ├── admin.py
│   ├── auth.py
│   ├── __init__.py
│   ├── logger.py
│   ├── models.py
│   ├── routes.py
│   ├── README.md
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── dashboard.js
│   │   └── vendor/
│   │       └── chart.js
│   └── templates/
│       ├── base.html
│       ├── dashboard.html
│       ├── login.html
│       ├── manage_users.html
│       └── unauthorized.html
│
├── config.py
├── instance/
│   └── sqlite.db
├── LICENSE
├── log_metrics.py
├── logs/
│   └── cron.log
├── migrations/
├── pyproject.toml
├── README.md
├── requirements.txt
├── run.py
├── test_fetch.py
├── tests/
│   ├── __init__.py
│   └── test_routes.py
└── venv/
```
