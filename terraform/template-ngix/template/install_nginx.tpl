#!/bin/bash
set -e
echo "*****    Installing Nginx    *****"
apt update
apt install -y nginx
ufw allow '${ufw_allow_nginx}'
systemctl enable nginx
systemctl restart nginx

echo "*****   Installation Complteted!!   *****"

echo "Welcome to Google Compute VM Instance deployed using Terraform!!!" > /var/www/html/index.html

echo "*****   Startup script completes!!    *****"
