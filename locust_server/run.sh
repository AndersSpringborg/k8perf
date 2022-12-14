docker network create --driver bridge locustnw
docker run --name server -p 80:80 -d --network="host" nginx 