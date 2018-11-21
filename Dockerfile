FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /src
ADD requirements.txt /src
RUN pip install -r /src/requirements.txt

COPY ./app /src/
WORKDIR /src

CMD ["gunicorn", "-c", "gunicorn.conf", "server:app"]
