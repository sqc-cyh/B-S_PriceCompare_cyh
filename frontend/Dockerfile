# 使用官方 Node.js 镜像
FROM node:slim

# 设置工作目录
WORKDIR /app

# 安装依赖
COPY package*.json ./
RUN npm install

# 复制项目文件
COPY . .

# 构建应用
RUN npm run build

# 启动应用
CMD ["npm", "run", "serve"]