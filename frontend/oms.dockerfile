FROM node:17-alpine

WORKDIR /app
COPY /package.json .
RUN npm install

EXPOSE 3000
COPY . ./

CMD ["npm", "start"]