FROM python:3.9



COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./webapp/FastAPI/api.py /code/api.py
COPY ./webapp/FastAPI/get_last_prediction.py /code/get_last_prediction.py
COPY ./Credentials/db_dev.json /code/db_dev.json

WORKDIR /code

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]
