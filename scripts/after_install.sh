#!/usr/bin/env bash

sudo chown -R ubuntu /home/ubuntu/project
cd /home/ubuntu/project

export PIPENV_VENV_IN_PROJECT=1
pipenv install

if [ $( grep -c 'SECRET_KEY' /home/ubuntu/.env ) = 0 ]; then
  pipenv run python genkey.py >> /home/ubuntu/.env
fi

cp /home/ubuntu/.env ./

pipenv run python manage.py makemigrations
pipenv run python manage.py collectstatic --no-input
pipenv run python manage.py migrate

sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl start gunicorn.service
sudo systemctl enable nginx
sudo systemctl enable gunicorn
sudo ufw allow 'Nginx Full'
sudo systemctl restart nginx
sudo systemctl restart gunicorn
