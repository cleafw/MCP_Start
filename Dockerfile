# Seeed MCP_Start Dockerfile
# 用于在目标设备上快速部署 MCP 服务

FROM python:3.11-slim

# 防止 Python 生成 .pyc 文件
ENV PYTHONDONTWRITEBYTECODE=1
# 设置非交互式、无缓冲输出
ENV PYTHONUNBUFFERED=1

# 安装系统依赖（浏览器相关）
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# 创建非 root 用户（避免权限问题）
RUN useradd -m -s /bin/bash recomputer \
    && echo "recomputer:12345678" | chpasswd \
    && adduser recomputer sudo

# 设置工作目录
WORKDIR /home/recomputer/Seeed/Project

# 复制依赖文件
COPY requirements.txt .
# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 设置所有者
RUN chown -R recomputer:recomputer /home/recomputer

# 切换到非 root 用户
USER recomputer

# 默认启动命令
ENTRYPOINT ["python", "main.py"]
