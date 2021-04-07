# Visual Inspection


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
