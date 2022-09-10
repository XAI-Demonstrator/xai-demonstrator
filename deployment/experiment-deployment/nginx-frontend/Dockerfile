FROM nginx:alpine

COPY ./nginx-frontend/nginx.conf /etc/nginx/nginx.conf

RUN rm -rf /usr/share/nginx/html/*

COPY  ./nginx-frontend/country/  /usr/share/nginx/html

ENTRYPOINT ["nginx", "-g", "daemon off;"]
