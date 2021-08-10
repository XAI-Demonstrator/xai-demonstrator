# Visual inspection explanation service

Build    | ![Visual Inspection](https://github.com/XAI-Demonstrator/xai-demonstrator/workflows/Visual%20Inspection/badge.svg?branch=master)
---------|-------
Backend  | [![Coverage Status](https://coveralls.io/repos/github/XAI-Demonstrator/xai-demonstrator/badge.svg?branch=x-cov-inspection-backend)](https://coveralls.io/github/XAI-Demonstrator/xai-demonstrator?branch=x-cov-inspection-backend)
Frontend | [![Coverage Status](https://coveralls.io/repos/github/XAI-Demonstrator/xai-demonstrator/badge.svg?branch=x-cov-inspection-frontend)](https://coveralls.io/github/XAI-Demonstrator/xai-demonstrator?branch=x-cov-inspection-frontend)

- **[Documentation](https://xai-demonstrator.github.io/xai-demonstrator/use-cases/visual-inspection/)**

## Components

- Predictions are provided by a [MobileNetV2 model](https://www.tensorflow.org/api_docs/python/tf/keras/applications/mobilenet_v2)
  pre-trained on ImageNet and fine-tuned on task-specific samples
- Backend microservice built with [FastAPI](https://fastapi.tiangolo.com/)
- Frontend created with [VueJS](https://vuejs.org/) utilizing the [Advanced Cropper](https://norserium.github.io/vue-advanced-cropper/) component

## Environment Variables

Defined in [inspection/config.py](./inspection-backend/inspection/config.py).

Variable | Description | Default Value
---------|-------------|--------------
`SERVICE_NAME` | The name that the app uses as its identifier, e.g. when logging or emitting traces | `"inspection-service"`
`ROOT_PATH` | FastAPI root path ([doc](https://fastapi.tiangolo.com/advanced/behind-a-proxy/)) | `""`
`PATH_PREFIX` | FastAPI router prefix ([doc](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies)) | `""`
`DEFAULT_EXPLAINER` | The explanation generator to use if a request does not speficy one | `"lime"`
`LOG_INPUT` | Save input images to disk | `False`
`LOG_PATH` | Path to store the logged images | `./log`