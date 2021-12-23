# Build frontend
FROM node:12.10.0-slim as builder

WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH

COPY package.json /app/package.json
RUN npm install --silent
COPY . /app
RUN npm run build

# Build a static version in a separate image
FROM nginx:1.17
COPY --from=builder /app/build /app/build

# # Copy nginx configuration
ADD nginx-entrypoint.sh /etc/nginx/conf.d/
ADD nginx-dev.conf.template /etc/nginx/conf.d/
ADD nginx.conf.template /etc/nginx/conf.d/
