#!/bin/bash
# filepath: /workspaces/watering/restart_watering_server.sh

# 停止并删除旧容器（如果存在）
docker stop watering-server 2>/dev/null
docker rm watering-server 2>/dev/null

# 删除旧镜像（如果存在）
docker rmi watering-server 2>/dev/null

# 重新构建镜像
docker build -t watering-server .

# 后台启动新容器

docker run -d -p 8080:8080 --name watering-server watering-server

echo "watering-server 已重新编译并后台启动。"