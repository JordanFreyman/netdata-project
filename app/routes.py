from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from sqlalchemy import desc
from .models import User, db, MetricLogs

main_bp = Blueprint('main', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.type != 'Admin':
            flash("Admins only!", "danger")
            return redirect(url_for('main.unauthorized'))
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route('/')
def index():
    return render_template('login.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/unauthorized')
def unauthorized():
    return render_template('unauthorized.html')

@main_bp.route('/manage_users', methods=['GET', 'POST'])
@admin_required
@login_required
def manage_users():
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
    from datetime import datetime, timedelta
    from flask import request

    if metric_type not in ['cpu', 'memory', 'disk', 'network']:
        return jsonify({"error": "Invalid metric type"}), 400

    metric_field = {
        'cpu': MetricLogs.cpu_usage,
        'memory': MetricLogs.memory_usage,
        'disk': MetricLogs.disk_usage,
        'network': MetricLogs.network_usage
    }[metric_type]

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

    logs = MetricLogs.query.filter(MetricLogs.timestamp >= start_time).order_by(MetricLogs.timestamp.asc()).all()

    grouped_data = {}
    for log in logs:
        machine = log.machine_name
        grouped_data.setdefault(machine, []).append({
            "timestamp": log.timestamp.isoformat(),
            "value": getattr(log, f"{metric_type}_usage")
        })

    return jsonify(grouped_data)
