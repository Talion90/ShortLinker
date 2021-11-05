FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/ShortLinkDjango
COPY . /usr/src/ShortLinkDjango/

RUN pip install -r /usr/src/ShortLinkDjango/requirements.txt

EXPOSE 8000