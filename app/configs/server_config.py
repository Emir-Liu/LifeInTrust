import os

# 服务的配置
server_ip = "127.0.0.1"
server_port = 8000

# 前端服务的配置,增加系统环境变量配置
FRONT_IP = os.getenv("FRONT_IP_ENV", "127.0.0.1")
FRONT_PORT = int(os.getenv("FRONT_PORT_ENV", "8000"))
FRONT_URL = os.getenv("FRONT_URL_ENV", "/update")
