#!/usr/bin/env bash

sudo apt update
sudo apt install -y ruby wget python3-pip python3-dev libpq-dev nginx postgresql postgresql-contrib
sudo apt -y autoremove
sudo pip3 install pipenv
cd /home/ubuntu

sudo rm -r /home/ubuntu/install
wget https://aws-codedeploy-ap-northeast-1.s3.amazonaws.com/latest/install
chmod +x ./install
sudo ./install auto

sudo rm -rf /home/ubuntu/project
sudo rm -f /etc/systemd/system/gunicorn.service
sudo rm -f /etc/systemd/system/gunicorn.socket
sudo rm -f /etc/nginx/conf.d/project.conf

mkdir -p /home/ubuntu/logs
