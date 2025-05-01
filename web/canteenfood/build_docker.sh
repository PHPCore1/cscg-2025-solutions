#!/bin/bash
docker rm -f canteenfood
docker build -t canteenfood . && \
docker run --name=canteenfood --rm -p 127.0.0.1:1337:80 -it canteenfood