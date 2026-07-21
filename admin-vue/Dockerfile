# 第一阶段：构建前端
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# 第二阶段：Nginx 运行
FROM nginx:stable-alpine
COPY --from=builder /app/dist /usr/share/nginx/html/admin
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
