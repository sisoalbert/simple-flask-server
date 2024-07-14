# gunicorn_config.py

bind = "0.0.0.0:8000"
workers = 3  # Adjust the number of workers based on your app's needs and server's capacity
accesslog = "-"
errorlog = "-"
loglevel = "info"
timeout = 120
