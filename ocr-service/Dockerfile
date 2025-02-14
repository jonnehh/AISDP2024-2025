# 使用官方 Python 3.12 slim 镜像作为基础镜像
FROM python:3.9-slim

# 禁用 PaddlePaddle IR 优化
ENV FLAGS_enable_ir_optim=false

# 更新 apt 并安装必要依赖库
RUN apt-get update && apt-get install -y libgl1-mesa-glx libgomp1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 升级 pip 到最新版本
RUN pip install --upgrade pip

# 复制依赖文件并安装依赖
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 复制所有代码到容器中
COPY . .

# 声明容器监听端口（假设 OCR 服务监听 5000 端口）
EXPOSE 5000

# 启动 Flask 应用（入口文件为 app.py）
CMD ["bash", "-c", "export FLAGS_enable_ir_optim=false && python app.py"]
