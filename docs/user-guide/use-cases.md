# Creating use cases

The [_XAI Demonstrator_](https://xai-demonstrator.github.io/) comprises a collection of fully independent use cases.
Each use case aims to illustrate a particular application of Explainable AI (XAI) methods.

On this page, we show you how to add another use case.
In the process, we discuss some of our fundamental design considerations and give an overview of the architecture. 

## What is a "use case"?

On a technical level, each use case consists of a user interface (frontend) paired with a stateless microservice (backend).

The frontend is a single-page web application (SPA) that the users interact with on their smartphone.
While the frontend is arguably the component most challenging to design, from a technical perspective, it's a fairly standard and lightweight web app.

The backend, on the other hand, is where the AI predictions and corresponding explanations are generated.
(Throughout this guide, we will assume that "the AI" is some sort of machine-learning model. 
In line with most common machine-learning frameworks, we will refer to all model outputs "predictions".)

The backend provides an HTTP-API that the frontend calls to request and receive predictions and explanations.
From a technical point of view, the frontend (that runs in the users' web browser) and the backend (which is hosted on a server somewhere "on the internet") are two separate entities.
Indeed, in the more advanced deployment configurations of the _XAI Demonstrator_, the two are usually not provided through the same service.

In this guide, however, we will take a designer's perspective and consider a use case as a unit.

!!! note "A note on code organization 💡"
 
    The entire code for the _XAI Demonstrator_ lives in one single Git repository, a so-called monorepo.
    Hence, you can just clone
    [the repository](https://www.github.com/xai-demonstrator/xai-demonstrator)
    and are good to go.
    
    Compared to the perhaps more traditional approach of keeping each use case in a separate repository, 
    a monorepo might at first seem daunting and overly complex.

    However, especially when working with a team of varying levels of experience (like [ours](/about/#team)),
    you will probably soon see how convenient it is to keep all the code in one place.

    Everyone can immediately see where changes have been made and how the different components relate to each other.
    It is also straightforward to [deploy](/user-guide/deployment) the _XAI Demonstrator_ to your local machine or some cloud infrastructure,
    as all the required scripts and configuration files live in the monorepo as well.

    _To learn more about why we chose this approach and what goes on behind the scenes, see [this tech note](/tech-notes/monorepo/)._

## Adding a use case

Each use case is self-contained and resides in its own top-level directory.
This directory contains the code for the backend and the frontend and the instructions on how to combine the two.

In the case that a use case builds on a custom machine learning model,
the code describing its training finds its place in the use case's directory as well.

Thus, the first step in adding a use case is to create a new directory at the root of the repository.
All _XAI Demonstrator_ use cases adhere to the following basic structure and naming convention,
which we recommend you follow as well:
```
use-case/
|
|- case-backend/  # (1)
|  |- case/
|  |  |- __init__.py
|  |  |- main.py
|  |
|  |- requirements.txt
|      
|- case-frontend/  # (2)
|  |- src/
|  |  |- App.vue
|  |
|  |- package.json
|     
|- Dockerfile  # (3)
|- README.md 
```
The most important elements, which we will instantiate in the following, are:
1. A microservice built with [FastAPI](https://fastapi.tiangolo.com/) (the backend).
2. A [VueJS](https://vuejs.org/) single-page application (the frontend).
3. A Dockerfile that describes how to assemble backend and frontend into a single container.

!!! note "A note on the _XAI Demonstrator_'s tech stack 💡"

    The _XAI Demonstrator_ use case backends are [FastAPI](https://fastapi.tiangolo.com/) microservices,
    while the frontends are [VueJS](https://vuejs.org/) single-page applications.
    Both frameworks are not only versatile and convenient, but are beginner-friendly choices.
    
    In principle, you can choose whatever programming language and framework you like for your use cases.
    As long as you provide a Docker container with an HTTP API and a corresponding web frontend, you're good to go.
     
    However, to fully benefit from the infrastructure and utilities the _XAI Demonstrator_ provides,
    we recommend you stay as close to its original tech stack as possible.

    _To learn more about how and why we selected these frameworks, see [this tech note](/tech-notes/tech-stack/)._

### Create the backend microservice

<!--
We use [FastAPI](https://fastapi.tiangolo.com/).

```bash
cd case-backend/
uvicorn case.main:app
```

You can access it at http://localhost:8000. -->

!!! warning "Use case backends should be stateless"
     
    All _XAI Demonstrator_ backends are stateless.
    In other words, each call to their API is self-contained:
    The response to a request does not depend on information from previous requests.

    This is an established approach to designing microservices
    that makes their development, testing, and monitoring straightforward.
    
    Further, it allows us to run multiple instances of the backends in parallel 
    and distribute the frontends' calls among them.
    In particular, it enables us to deploy the _XAI Demonstrator_ to a serverless infrastructure.
    (Don't worry if at this point you have no idea what that means.)
    
    We strongly recommend that you design your backends to be stateless as well.

### Create the frontend

<!-- We use [VueJS](https://vuejs.org/). Generally with Mint-UI components. 

```bash
cd use-case
vue-cli case-frontend
```

This generates the basic structure.
You can immediately test that everything was set up correctly:
```bash
cd case-frontend/
npm run
```
You can access it at http://localhost:8080. -->

!!! warning "Serving the frontend"
    
    To be able to operate a use case on its own, in addition to delivering predictions and explanations,
    the backend needs to deliver the frontend to the user's browser.
    
    The `xaidemo` package provides a helper function that generates the necessary routes:
     
        from xaidemo.routers import vue_frontend
        
        app = FastAPI()
        app.include_router(vue_frontend(__file__))

    Note that this requires ... . See the next section.

### Assemble the use case

All of this can be described in a single _Dockerfile_, which :

```dockerfile
# FIRST STAGE
FROM node:12-alpine as builder
WORKDIR /

# Copy the frontend code into the container
COPY ./case-frontend/ .

# Install frontend dependencies and build the frontend
RUN npm install && npm run build


# SECOND STAGE
FROM python:3.8-slim
WORKDIR /

# Copy the backend code
COPY case-backend/case /case

# Install all Python dependencies
COPY case-backend/requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt \
    && rm -rf /root/.cache/pip

# Copy the frontend from the first stage
RUN mkdir /case/static
COPY --from=builder /dist/ /case/static/

# Launch backend service
CMD ["uvicorn", "case.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

With this Docker file, the use case can be built and started:
```bash
cd use-case
docker run
```

## What's next?
