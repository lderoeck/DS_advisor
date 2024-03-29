#!/usr/bin/env bash

# Update apt
sudo apt-get update
# Install deps
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

# Get docker image
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update

# Install docker
sudo apt-get install docker-ce docker-ce-cli containerd.io

# Install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# chmod all the things
chmod 777 ./services/vehicles/entrypoint.sh
chmod 777 ./services/stops/entrypoint.sh
chmod 777 ./services/users/entrypoint.sh

# Create containers and run
sudo docker-compose -f ./docker-compose-dev.yml up -d --build
# Create database tables
sudo docker-compose -f ./docker-compose-dev.yml run vehicles python manage.py recreate-db
# Open webbrowser
xdg-open http://127.0.0.1:5000
