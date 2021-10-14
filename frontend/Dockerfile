FROM node:14.17.0-buster

WORKDIR /usr/src/app

COPY .env .
COPY .env.development.local .
COPY package.json .
COPY yarn.lock .
RUN yarn --pure-lockfile
RUN yarn global add react-scripts@4.0.3

CMD ["yarn", "start"]