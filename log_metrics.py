#!/usr/bin/env python3
import sys
sys.path.insert(0, "/root/lynis/cop4521-flask")

from app import create_app
from app.logger import log_metrics

app = create_app()

with app.app_context():
    log_metrics()
