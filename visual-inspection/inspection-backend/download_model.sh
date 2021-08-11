#!/usr/bin/env bash

cd ./inspection/model || exit 1
curl https://storage.googleapis.com/xai-demonstrator-assets/visual-inspection/models/my_model.zip -o my_model.zip
unzip -o my_model.zip
rm my_model.zip
