"""Main application routes for dashboard, user management, and API metrics."""

from datetime import datetime, timedelta, timezone
from functools import wraps

from flask import (
    Blueprint, render_template, request, flash,
    redirect, url_for, jsonify
)
from flask_login import login_required, current_user

from .models import User, db, MetricLogs

main_bp = Blueprint('main', __name__)


def admin_required(f):
    """Custom decorator to restrict access to admin users."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.type != 'Admin':
            flash("Admins only!", "danger")
            return redirect(url_for('main.unauthorized'))
        return f(*args, **kwargs)
    return decorated_function


@main_bp.route('/')
def index():
    """Render the login page."""
    return render_template('login.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Render the user dashboard with info about unreachable machines."""
    from sqlalchemy import func

    cutoff = datetime.now(timezone.utc) - timedelta(hours=1)
    subquery = (
        db.session.query(
            MetricLogs.machine_name,
            func.max(MetricLogs.timestamp).label("latest")
        )
        .filter(MetricLogs.timestamp >= cutoff)
        .group_by(MetricLogs.machine_name)
        .subquery()
    )

    recent_logs = (
        db.session.query(MetricLogs)
        .join(subquery, db.and_(
            MetricLogs.machine_name == subquery.c.machine_name,
            MetricLogs.timestamp == subquery.c.latest
        ))
        .all()
    )

    unreachable = [
        log.machine_name for log in recent_logs
        if all(getattr(log, field) is None for field in [
            'cpu_usage', 'memory_usage', 'disk_usage', 'network_usage'
        ])
    ]

    return render_template('dashboard.html', unreachable=unreachable)


@main_bp.route('/unauthorized')
def unauthorized():
    """Render unauthorized access page."""
    return render_template('unauthorized.html')


@main_bp.route('/manage_users', methods=['GET', 'POST'])
@admin_required
@login_required
def manage_users():
    """Allow admins to manage users and assign roles."""
    if request.method == 'POST':
        email = request.form.get('email')
        user_type = request.form.get('user_type', 'User')
        if email:
            user = User.query.filter_by(email=email).first()
            if user:
                user.type = user_type
            else:
                user = User(username=email.split('@')[0], email=email, type=user_type)
                db.session.add(user)
            db.session.commit()
            flash('User updated successfully.', 'success')

    users = User.query.all()
    return render_template('manage_users.html', users=users)


@main_bp.route('/api/metrics/<string:metric_type>')
@login_required
def get_metric_data(metric_type):
    """API endpoint to retrieve grouped metrics by machine and timestamp."""
    if metric_type not in ['cpu', 'memory', 'disk', 'network']:
        return jsonify({"error": "Invalid metric type"}), 400

    range_param = request.args.get('range', '1h')
    now = datetime.now(timezone.utc)

    if range_param == '1h':
        start_time = now - timedelta(hours=1)
    elif range_param == '24h':
        start_time = now - timedelta(hours=24)
    elif range_param == '7d':
        start_time = now - timedelta(days=7)
    else:
        start_time = now - timedelta(hours=1)

    logs = (
        MetricLogs.query
        .filter(MetricLogs.timestamp >= start_time)
        .order_by(MetricLogs.timestamp.asc())
        .all()
    )

    grouped_data = {}
    for log in logs:
        grouped_data.setdefault(log.machine_name, []).append({
            "timestamp": log.timestamp.isoformat(),
            "value": getattr(log, f"{metric_type}_usage")
        })

    return jsonify(grouped_data)
