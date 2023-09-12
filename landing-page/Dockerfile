FROM node:14-alpine as builder14

RUN mkdir /frontend
WORKDIR /frontend
COPY ./landing-page/frontend .
RUN npm install && npm run build -- --mode test-deployment

RUN mkdir /sentiment
WORKDIR /sentiment
COPY ./review-sentiment/sentiment-frontend/ .
RUN npm install && npm run build -- --mode test-deployment

RUN mkdir /inspection
WORKDIR /inspection
COPY ./visual-inspection/inspection-frontend/ .
RUN npm install && npm run build -- --mode visual-inspection.test-deployment

RUN mkdir /education
WORKDIR /education
COPY ./visual-inspection/inspection-frontend/ .
RUN npm install && npm run build -- --mode digital-education.test-deployment

FROM node:18-alpine as builder18

RUN mkdir /country
WORKDIR /country
COPY ./guess-the-country/country-frontend/ .
RUN npm install && npm run build -- --mode test-deployment

FROM nginx:alpine

COPY ./landing-page/nginx.conf /etc/nginx/nginx.conf

RUN rm -rf /usr/share/nginx/html/*

COPY --from=builder14 /frontend/dist/ /usr/share/nginx/html
RUN mkdir /usr/share/nginx/html/sentiment \
    && mkdir /usr/share/nginx/html/inspection \
    && mkdir /usr/share/nginx/html/country \
    && mkdir /usr/share/nginx/html/education
COPY --from=builder14 /sentiment/dist/ /usr/share/nginx/html/sentiment
COPY --from=builder14 /inspection/dist/ /usr/share/nginx/html/inspection
COPY --from=builder14 /education/dist/ /usr/share/nginx/html/education
COPY --from=builder18 /country/dist/ /usr/share/nginx/html/country

ENTRYPOINT ["nginx", "-g", "daemon off;"]
