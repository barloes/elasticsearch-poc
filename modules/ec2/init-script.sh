Content-Type: multipart/mixed; boundary="//"
MIME-Version: 1.0

--//
Content-Type: text/cloud-config; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="cloud-config.txt"

#cloud-config
cloud_final_modules:
- [scripts-user, always]

--//
Content-Type: text/x-shellscript; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="userdata.txt"

#!/bin/bash

sudo apt-get update
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    awscli -y

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install \
    docker-ce \
    docker-ce-cli \
    containerd.io -y

sudo curl -L "https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-linux-aarch64" -o /usr/local/bin/docker-compose
sudo chmod +rwx /usr/local/bin/docker-compose
sudo chmod 666 /var/run/docker.sock
sudo service docker start

cd ~
sudo rm -rf ~/*

aws s3 cp s3://${NAME}/${PROJECT_NAME}.tar.gz ./${PROJECT_NAME}.tar.gz

tar -xvf ${PROJECT_NAME}.tar.gz

sudo aws ecr get-login-password --region ${AZ} | docker login --username AWS --password-stdin ${AWS_ID}
docker pull ${AWS_ID}/${NAME}:${PROJECT_NAME}

docker-compose build && docker-compose up -d
--//--