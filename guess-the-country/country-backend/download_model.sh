#!/usr/bin/env bash

cd ./country/model || exit 1
curl https://storage.googleapis.com/xai-demo-assets/guess-the-country/models/my_model.zip -o my_model.zip
unzip -o my_model.zip
rm my_model.zip
