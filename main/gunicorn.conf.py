import os
# bind = os.getenv("GUNICORN", "0.0.0.0:8000")
workers = 3 # Adjust the number of workers as needed
name = "main"
timeout = 120
log_level = "debug"
log_file = "/var/log/gunicorn_error.log" # always empty. Why?
access_logfile = "/var/log/gunicorn_access.log" # always empty. Why?
# Django log is defined in settings.py
