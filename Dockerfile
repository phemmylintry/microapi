# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8

# Keeps Python from generating .pyc files in the container
# ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
    && apt-get install -y mariadb-client \
    && rm -rf /var/lib/apt/lists/*

# Install pip requirements
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app
ADD . /app
COPY . /app

#COPY ./.env /app/.env
# COPY env.example /app/.env

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
# RUN useradd appuser && chown -R appuser /app
RUN mkdir -p /app/static/
RUN python manage.py collectstatic --noinput

COPY ./wait-for-it.sh /usr/wait-for-it.sh
RUN chmod +x /usr/wait-for-it.sh

#run migrations
# RUN python manage.py makemigrations && python manage.py migrate --noinput

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "microapi_dashboard.wsgi"]