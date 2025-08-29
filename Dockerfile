FROM ubuntu:24.04
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq -y \
    && apt-get install -y binutils libproj-dev python3-gdal libgeos-dev libyaml-dev python3-pip \
    && apt-get clean \
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --target=packages -r requirements.txt

COPY . /app
RUN useradd django
RUN chown -R django:django /app
WORKDIR /app

EXPOSE 8000
# Run the production server
CMD gunicorn --bind 0.0.0.0:$PORT --access-logfile - vbos.wsgi:application
