#!/usr/bin/env bash

cd ./country-frontend/ || exit 1
npm run test:unit
npm run build
cd ..

rm -r ./country-backend/country/static/* || mkdir ./country-backend/country/static/
cp -r ./country-frontend/dist/* ./country-backend/country/static/
