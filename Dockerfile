FROM node:alpine
ENV NODE_ENV production
WORKDIR /usr/src/app
COPY ["dist", "./"]
RUN npm install -g serve
EXPOSE 80
CMD serve -s -l 80 ./