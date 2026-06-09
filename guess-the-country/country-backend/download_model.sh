#!/usr/bin/env bash
set -euo pipefail

mkdir -p country/model
cd country/model || exit 1

curl -fsSL https://storage.googleapis.com/xai-demo-assets/guess-the-country/models/my_model.zip -o my_model.zip
unzip -o my_model.zip
rm -f my_model.zip
