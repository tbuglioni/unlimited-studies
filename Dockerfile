FROM python:3.8-alpine

WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]