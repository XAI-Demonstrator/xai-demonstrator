# Visual Explanations

| Build    | ![Visual Inspection](https://github.com/XAI-Demonstrator/xai-demonstrator/workflows/Visual%20Inspection/badge.svg?branch=master)                                                                                                     |
|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Backend  | [![Coverage Status](https://coveralls.io/repos/github/XAI-Demonstrator/xai-demonstrator/badge.svg?branch=x-cov-inspection-backend)](https://coveralls.io/github/XAI-Demonstrator/xai-demonstrator?branch=x-cov-inspection-backend)   |
| Frontend | [![Coverage Status](https://coveralls.io/repos/github/XAI-Demonstrator/xai-demonstrator/badge.svg?branch=x-cov-inspection-frontend)](https://coveralls.io/github/XAI-Demonstrator/xai-demonstrator?branch=x-cov-inspection-frontend) |

## Components

- Predictions are provided by a [MobileNetV2 model](https://www.tensorflow.org/api_docs/python/tf/keras/applications/mobilenet_v2)
  pre-trained on ImageNet and fine-tuned on task-specific samples
- Backend microservice built with [FastAPI](https://fastapi.tiangolo.com/)
- Frontend created with [VueJS](https://vuejs.org/) utilizing the [Advanced Cropper](https://norserium.github.io/vue-advanced-cropper/) component

## Environment Variables

Variable | Description | Default Value
---------|-------------|--------------
`SERVICE_NAME` | The name that the app uses as its identifier, e.g. when logging or emitting traces | `"inspection-service"`
`ROOT_PATH` | FastAPI root path ([doc](https://fastapi.tiangolo.com/advanced/behind-a-proxy/)) | `""`
`PATH_PREFIX` | FastAPI router prefix ([doc](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies)) | `""`
`DEFAULT_EXPLAINER` | The explanation generator to use if a request does not speficy one | `"lime"`
`LOG_INPUT` | Save input images to disk | `False`
`LOG_PATH` | Path to store the logged images | `./log`

## Running the service locally (with Docker)

To launch a standalone instance of the service:

```shell
cd visual-inspection
docker-compose up
```

## Running the service locally (without Docker)

During development, it can be desirable to launch the service directly and not as a Docker container.
For instance, this allows to get rapid feedback on changes to the backend code.

```shell
cd visual-inspection
./build_frontend.sh
cd inspection-backend
uvicorn inspection.main:app
```

## Log input images

For development purposes, the service can be configured to write the raw input images to disk.
This setting is controlled through the environment variable `LOG_INPUT`:
```shell
export LOG_INPUT=1
```

By default, the images are collected in a sub-folder `./log`.
To change where the images are saved to, set the environment variable `LOG_PATH`, e.g.:
```shell
export LOG_PATH=/home/myusername/log
```
