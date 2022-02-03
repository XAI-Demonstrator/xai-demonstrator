FROM nginx:alpine

COPY ./nginx.conf /etc/nginx/nginx.conf

RUN rm -rf /usr/share/nginx/html/*

COPY --from=builder ./frontend/country-frontend/ /usr/share/nginx/html
# RUN mkdir /usr/share/nginx/html/country/
# COPY --from=builder ./gtc-nginx/frontend/ /usr/share/nginx/html/country

ENTRYPOINT ["nginx", "-g", "daemon off;"]