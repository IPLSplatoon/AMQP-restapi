FROM python:3.13
ARG PORT=2000
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./restapi /code/restapi

CMD ["fastapi", "run", "restapi/main.py", "--port", "2000"]
EXPOSE ${PORT}