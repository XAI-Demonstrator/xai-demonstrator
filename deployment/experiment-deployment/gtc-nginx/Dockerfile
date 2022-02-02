FROM nginx:alpine

COPY ./gtc-nginx/nginx.conf /etc/nginx/nginx.conf

RUN rm -rf /usr/share/nginx/html/*

COPY --from=builder /frontend/dist/ /usr/share/nginx/html
RUN mkdir /usr/share/nginx/html/country
COPY --from=builder /country/dist/ /usr/share/nginx/html/country

ENTRYPOINT ["nginx", "-g", "daemon off;"]
