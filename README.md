```commandline
docker build -t backend .
docker run --restart always -d -p 8051:8000 backend:latest
```