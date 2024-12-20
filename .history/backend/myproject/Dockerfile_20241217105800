# 使用官方 Python 镜像
FROM python:3.12

# 设置工作目录
WORKDIR /app


# 安装依赖
RUN apt-get update && apt-get install -y libgl1
# RUN apt-get update && apt-get install -y libgl1 unzip
# RUN wget https://msedgedriver.azureedge.net/132.0.2957.48/edgedriver_linux64.zip\
#     && unzip edgedriver_linux64.zip -d /usr/local/bin/ \
#     && chmod +x /usr/local/bin/msedgedriver \
#     && echo "Download successful"
# 复制项目文件到工作目录
COPY . .  
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r ./requirements.txt   



# 运行迁移
# RUN python ./myproject/manage.py makemigrations
# RUN python ./myproject/manage.py migrate
# RUN python ./myproject/manage.py runserver

# 启动 Django 服务器
CMD ["python", "./myproject/manage.py", "runserver", "0.0.0.0:8000"]