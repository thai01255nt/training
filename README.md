```commandline
docker build -t backend .
docker network create fullStack
docker run --network fullStack --name docker-api --restart always -d -p 8051:8000 backend:latest
```