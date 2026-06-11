FROM node:20-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install --registry=https://registry.npmmirror.com
COPY . .

ARG API_BASE=/api
ENV NUXT_PUBLIC_API_BASE=$API_BASE

RUN npm run build

EXPOSE 3000
CMD ["node", ".output/server/index.mjs"]
