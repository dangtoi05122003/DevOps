FROM node:18.20.3
ENV MONGO_DB_USERNAME=admin \
    MONGO_DB_PASSWORD=123
RUN mkdir -p /home/app
COPY . /home/app

CMD ["node", "/home/app/server.js"]