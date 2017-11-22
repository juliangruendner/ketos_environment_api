if [[ "$(docker images -q alpine_jupyter:latest 2> /dev/null)" == "" ]]; then
  docker build -t alpine_jupyter ./docker
fi

docker-compose -f docker/docker-compose.yml -f docker/docker-compose.prod.yml up -d
