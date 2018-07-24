#! /bin/sh

docker container prune -f
docker image prune -a -f
docker volume ls -qf dangling=true | xargs -r docker volume rm
rm -rf /var/log/messages*
rm -rf /var/log/mesos

# docker system prune