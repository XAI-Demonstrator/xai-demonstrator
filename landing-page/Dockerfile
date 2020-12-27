FROM node:12-alpine as builder

RUN mkdir /frontend
WORKDIR /frontend
COPY ./landing-page/frontend .
RUN npm install && npm run build

RUN mkdir /sentiment
WORKDIR /sentiment
COPY ./review-sentiment/sentiment-frontend/ .
RUN npm install && npm run build -- --mode test-deployment

RUN mkdir /inspection
WORKDIR /inspection
COPY ./visual-inspection/inspection-frontend/ .
RUN npm install && npm run build -- --mode test-deployment

FROM nginx:alpine

COPY ./landing-page/nginx.conf /etc/nginx/nginx.conf

RUN rm -rf /usr/share/nginx/html/*

COPY --from=builder /frontend/dist/ /usr/share/nginx/html
RUN mkdir /usr/share/nginx/html/sentiment && mkdir /usr/share/nginx/html/inspection
COPY --from=builder /sentiment/dist/ /usr/share/nginx/html/sentiment
COPY --from=builder /inspection/dist/ /usr/share/nginx/html/inspection

ENTRYPOINT ["nginx", "-g", "daemon off;"]
