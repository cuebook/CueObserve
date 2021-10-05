# Build frontend
FROM node:12-slim as builder

WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH

COPY package.json /app/
RUN npm install --silent
COPY . /app/
RUN npm run build


# Build a static version in a separate image
FROM nginx:1.17
COPY --from=builder /app/build /app/build

# # Copy nginx configuration
ADD /app/nginx.conf /etc/nginx/conf.d/default.conf
