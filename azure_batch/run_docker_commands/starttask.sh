#!/bin/bash

echo "_azbatch ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/azbatch 
chmod 440 /etc/sudoers.d/azbatch
apt install -y docker.io
apt install -y docker-compose 
apt install -y gnupg2 pass
