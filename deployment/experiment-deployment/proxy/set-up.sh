#!/usr/bin/env bash

# See https://github.com/buchdag/letsencrypt-nginx-proxy-companion-compose

sudo docker network create nginx-proxy || echo "Network exists already!"

sudo docker-compose down
sudo docker-compose up -d
