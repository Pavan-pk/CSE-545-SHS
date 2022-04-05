#!/bin/sh
gunicorn --worker-class=gevent --worker-connections=3333 --workers=3 main:app

#gunicorn -w 3 -b 0.0.0.0:80 --chdir /app/hms_backend/api/  main:app