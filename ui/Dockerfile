# Build frontend
FROM node:12-slim as builder

WORKDIR /usr/src/app
COPY package.json ./
RUN yarn install --silent
COPY . ./
RUN yarn build

# Build a static version in a separate image
FROM nginx:1.17
WORKDIR /usr/src/app

# Copy nginx configuration
COPY --from=builder /usr/src/app/build ./build

ADD nginx.conf /etc/nginx/conf.d/default.conf
