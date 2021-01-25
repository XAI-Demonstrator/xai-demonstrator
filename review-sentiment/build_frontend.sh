#!/usr/bin/env bash

cd ./sentiment-frontend/ || exit 1
npm run build
cd ..

rm -r ./sentiment-backend/sentiment/static/* || mkdir ./sentiment-backend/sentiment/static
cp -r ./sentiment-frontend/dist/* ./sentiment-backend/sentiment/static/
