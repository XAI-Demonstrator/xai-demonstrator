# Customer review sentiment explanation service
![Review Sentiment](https://github.com/XAI-Demonstrator/template-service/workflows/Review%20Sentiment/badge.svg)


## Components

- Multilingual sentiment analysis provided by [NLPTown's bert-base-multilingual-uncased-sentiment]([https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment) model
- Explanations generated via Facebook's [Captum](https://captum.ai/) library
- Backend microservice built with [FastAPI](https://fastapi.tiangolo.com/)
- Frontend created with [VueJS](https://vuejs.org/) using [Mint UI](https://mint-ui.github.io/) components

## GPU Acceleration with CUDA
- The sentiment service can be run with GPU acceleration using Pytorch's [CUDA package](https://pytorch.org/docs/stable/cuda.html).
- In order to enable GPU support build the service from CUDA_Dockerfile.
- There are compatibilty conditions which need to be satisfied for CUDA to work.
- Firstly CUDA requires the installation of NVIDIA drivers. The drivers have to be supported by the utilized CUDA version. An overview of the minimum driver required for a specific version of CUDA can be found [here](https://docs.nvidia.com/deploy/cuda-compatibility/index.html#binary-compatibility__table-toolkit-driver).
- Secondly the PyTorch version has to be compatible with the CUDA version. A list of previous PyTorch versions, their supported CUDA versions and download instructions can be found [here](https://pytorch.org/get-started/previous-versions/).
- The configuration has been tested using NVIDIA driver version 410.104, CUDA 10.0 and PyTorch 1.4.0.
