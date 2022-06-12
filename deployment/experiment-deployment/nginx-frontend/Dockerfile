FROM nginx:alpine

COPY ./nginx-frontend/nginx.conf /etc/nginx/nginx.conf

RUN rm -rf /usr/share/nginx/html/*

COPY  ./nginx-frontend/education/  /usr/share/nginx/html
# RUN mkdir /usr/share/nginx/html/country/
# COPY --from=builder ./gtc-nginx/frontend/ /usr/share/nginx/html/country

ENTRYPOINT ["nginx", "-g", "daemon off;"]