#!/usr/bin/env bash

cd ./inspection/model || exit 1
mkdir models && cd models || exit 1

for model_id in "$@"
do
  curl "https://storage.googleapis.com/xai-demo-assets/visual-inspection/models/${model_id}.zip" -o "${model_id}.zip"
  unzip -o "${model_id}.zip"
  rm "${model_id}.zip"
done

