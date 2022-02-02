FROM node:14-alpine as builder

RUN mkdir /country
WORKDIR /country
COPY ./guess-the-country/country-frontend/ .
RUN npm install && npm run build -- --mode experiment-deployment

FROM nginx:alpine

COPY ./gtc-nginx/nginx.conf /etc/nginx/nginx.conf

RUN rm -rf /usr/share/nginx/html/*

COPY --from=builder /frontend/dist/ /usr/share/nginx/html
RUN mkdir /usr/share/nginx/html/country
COPY --from=builder /country/dist/ /usr/share/nginx/html/country

ENTRYPOINT ["nginx", "-g", "daemon off;"]
