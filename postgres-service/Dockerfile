# 使用官方 Python 3.12 作为基础镜像
FROM python:3.12

# 设置工作目录
WORKDIR /app

# 复制当前目录所有文件到容器中
COPY . .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 指定 Flask 运行端口
EXPOSE 5000

# 运行 Flask API
CMD ["python", "app.py"]
