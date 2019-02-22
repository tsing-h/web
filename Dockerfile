# stage 1: 制作一个build镜像
FROM node:alpine AS vue-cli
WORKDIR /code
RUN npm install -g cnpm --registry=https://registry.npm.taobao.org
RUN cnpm install -g @vue/cli
# 通过.dockerignore避免复制不必要的文件
COPY . /code
RUN cnpm install
RUN cnpm run build

# stage 2: 制作service镜像
FROM node:alpine
ENV NODE_ENV production
WORKDIR /usr/src/app
COPY --from=vue-cli /code/dist ./
RUN npm install -g serve
EXPOSE 80
CMD serve -s -l 80 ./