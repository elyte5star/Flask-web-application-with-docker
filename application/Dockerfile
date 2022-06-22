FROM python:3.10-slim-buster
WORKDIR /usr
COPY . .
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "app.py" ]
EXPOSE 3000