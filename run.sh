docker volume create --name=d54-data
docker volume create --name=organon-data

cp /home/ubuntu/.kube/config kubernetes

docker-compose up

sudo rm -r .kube

