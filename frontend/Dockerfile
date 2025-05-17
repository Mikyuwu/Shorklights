FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

RUN npm install vite --save-dev

EXPOSE 5173

CMD npm run dev -- --host 0.0.0.0 --port ${FRONTEND_PORT}