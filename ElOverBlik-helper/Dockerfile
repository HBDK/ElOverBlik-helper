FROM python:3-slim

WORKDIR /app

COPY ./App/*.py /app/
COPY ./App/requirements.txt /app/

RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["python", "main.py"]