bind = "0.0.0.0:8003" # can not be 80 as normal user
workers = 3 # Adjust the number of workers as needed
name = "main"
timeout = 120
log_level = "debug"
log_file = "/var/log/gunicorn3_error.log" # always empty. Why?
access_logfile = "/var/log/gunicorn3_access.log" # always empty. Why?
# Django log is defined in settings.py
# Do not forget to source .env before starting gunicorn
