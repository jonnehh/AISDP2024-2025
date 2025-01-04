# 使用官方 Python 基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制应用代码到工作目录
COPY app.py app.py
COPY requirements.txt requirements.txt
COPY templates/ templates/
COPY static/ static/

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露 Flask 使用的端口
EXPOSE 5000

# 启动 Flask 应用
CMD ["python", "app.py"]
