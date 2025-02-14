# 使用官方 Python 3.9 slim 镜像作为基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app
RUN pip install --upgrade pip
# 复制依赖文件并安装依赖
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 复制所有代码到容器中
COPY . .


EXPOSE 5050

# 启动 Flask 应用（入口文件为 app.py）
CMD ["python", "app.py"]
