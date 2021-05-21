# Getting started



## Get the source code

To develop your own use cases and contribute to the _XAI Demonstrator_
you need the software tool *Git* to manage your source code files.
*Git* is a so-called version control system that keeps track of all
the changes that are made and enables teams to work on the same piece
of software without making a mess.

Don't worry if you've never used *Git* before.
In this tutorial, we'll show you all the commands you need in detail.

!!! note "Installing Git"

    To install *Git*, see the instructions [here](./dev-setup/#install-git)

!!! note "Downloading without Git"

    If you just want to quickly try out the _XAI Demonstrator_ and
    do not have Git installed, you can simply download the source code
    [as a ZIP file]().

    However, please note that without Git **you will not be able to
    run use cases locally,** because Python dependencies are installed
    through Git.

    Thus, you are restricted to launching deployment configurations that
    utilize pre-built container images (more on that in the next section).

To download ("check out") the _XAI Demontrator_ source code from GitHub,
open a terminal (on Windows, we recommend *Git Bash*)
```bash
git clone https://github.com/xai-demonstrator/xai-demonstrator.git
```

After a couple of seconds, you'll find  the entire _XAI Demonstrator_ source
code in a new folder called `xai-demonstrator`.

## Install Docker

All parts of the _XAI Demonstrator_ are packaged and run as Docker containers.
These are best thought of as self-contained units that contain all required
dependencies and runtimes.

To run the _XAI Demonstrator_ or individual use cases locally, you need to install
Docker (but nothing else).
Docker is available for all common operating systems.
See [the instructions in the Docker documentation](https://docs.docker.com/engine/install/)
to learn how to install _Docker Engine_ on your local machine.
Make sure you install the `docker-compose` utility as well.

## Run your very own XAI Demonstrator instance

To launch the full _XAI Demonstrator_, you can use the `test-local` configuration:

```bash
cd xai-demonstrator/deployments/test-local
docker-compose up
```

!!! warning "Download size"

    This will download several GB of files from the GitHub Container Registry! 

After the downloads completed and the containers are spun up, you can visit your
very own _XAI Demonstrator_ at [http://localhost:8000/](http://localhost:8000/).

We used only a very small part of the source code:
```bash
cat docker-compose.yml
```

## Run a single use case

What does it do?

```bash
cd xai-demonstrator/visual-inspection
docker build .
docker run .
```

You can take a look at the `Dockerfile`, we'll get to that in
more detail later.

## Modify a use case

(Make a small change to the frontend.)

## What's next?

Congratulations!
You have not only set up everything that's necessary to run your very
own _XAI Demonstrator_, but already  a use case. 
