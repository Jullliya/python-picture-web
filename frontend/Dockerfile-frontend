FROM node:16

RUN npm install -g @vue/cli@~5.0.0

WORKDIR /front

COPY package.json .

RUN npm install

COPY . .

EXPOSE 8080

CMD ["npm", "run", "serve"]