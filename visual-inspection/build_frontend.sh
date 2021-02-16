#!/usr/bin/env bash

cd ./inspection-frontend/ || exit 1
npm run test:unit
npm run build
cd ..

rm -r ./inspection-backend/inspection/static/* || mkdir ./inspection-backend/inspection/static/
cp -r ./inspection-frontend/dist/* ./inspection-backend/inspection/static/
