FROM python:3.9.2

RUN pip install --upgrade pip
COPY ./ ./
RUN pip install -r requirements.txt
RUN pip install gunicorn
