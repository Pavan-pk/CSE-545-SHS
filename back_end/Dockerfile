FROM python:3.9.10-slim-buster

WORKDIR /app

copy . /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

#CMD ["python", "hms_backend/api/main.py"]

ENTRYPOINT ["./deployment/gunicorn_starter.sh"]