# Customer review sentiment explanation service

A microservice built with [FastAPI](https://fastapi.tiangolo.com/).

## Components

- Multilingual sentiment analysis provided by [NLPTown's bert-base-multilingual-uncased-sentiment]([https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment) model
- Explanations generated via Facebook's [Captum](https://captum.ai/) library
- Frontend created with [VueJS](https://vuejs.org/) using [Mint UI](https://mint-ui.github.io/) components
