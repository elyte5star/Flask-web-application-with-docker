FROM python:3.10-slim-buster
WORKDIR /usr
COPY ./application .
COPY ./application/requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip freeze
CMD [ "python", "app.py" ]
EXPOSE 3000