FROM node:14-alpine as builder

RUN mkdir /country
WORKDIR /country
COPY ./guess-the-country/country-frontend/ .
RUN npm install && npm run build -- --mode test-deployment

FROM nginx:alpine

COPY ./gtc-nginx/nginx.conf /etc/nginx/nginx.conf

RUN rm -rf /usr/share/nginx/html/*

COPY --from=builder ./gtc-nginx/frontend/country-frontend/ /usr/share/nginx/html
# RUN mkdir /usr/share/nginx/html/country/
# COPY --from=builder ./gtc-nginx/frontend/ /usr/share/nginx/html/country

ENTRYPOINT ["nginx", "-g", "daemon off;"]