# Getting started

This guide describes how to download the source code, launch your very own
_XAI Demonstrator_ instance and make a first change.

## Get the source code

To develop your own use cases and contribute to the _XAI Demonstrator_ project
you need the software tool _Git_ to manage your source code files.
_Git_ is a so-called [version control system](https://en.wikipedia.org/wiki/Version_control)
that keeps track of all the changes that are made and enables teams to work
on the same piece of software without making a mess.

Don't worry if you've never used _Git_ before.
In this tutorial, we'll show you all the commands you need in detail.

!!! note "Installing Git"

    To install _Git_, see the instructions [here](./dev-setup/#install-git).

!!! note "Downloading without Git"

    If you just want to quickly try out the _XAI Demonstrator_ and
    do not have _Git_ installed, you can simply download the source code
    [as a ZIP file](https://github.com/XAI-Demonstrator/xai-demonstrator/archive/refs/heads/master.zip).

    However, please note that without _Git_ **you will not be able to
    run use cases locally,** because some of the Python dependencies are
    installed through _Git_.

    Thus, you are restricted to launching deployment configurations that
    utilize pre-built container images (more on that in the next section).

To download ("check out") the _XAI Demontrator_ source code from GitHub,
open a terminal (on Windows, we recommend the _Git Bash_ that ships with _Git_),
navigate to the folder you'd like to store the source code in, and run the
following _Git_ command:

```bash
git clone https://github.com/xai-demonstrator/xai-demonstrator.git
```

After a couple of seconds, you'll find  the entire _XAI Demonstrator_ source
code in a new folder called `xai-demonstrator`.

## Install Docker

All parts of the _XAI Demonstrator_ are packaged and run as Docker containers.
These are best thought of as self-contained units that contain all required
dependencies and runtimes.

!!! note "Docker containers and images"
    
    Readers familar with _Docker_ terminology might note and perhaps object to
    our use of the term "container" to refer to both the "Docker image" and
    the "Docker container".

    This is not an oversight, but an intentional simplification. We will
    distinguish between the two when it becomes necessary later.

To run the _XAI Demonstrator_ or individual use cases locally on your computer,
you need to install Docker (but nothing else).
Docker is available for all common operating systems.
See [the instructions in the Docker documentation](https://docs.docker.com/engine/install/)
to learn how to install _Docker Engine_ on your computer.
Make sure you install the `docker-compose` utility as well.

## Run your very own XAI Demonstrator instance

To launch the full _XAI Demonstrator_, you can use the `test-local` deployment 
configuration. To launch this most minimal version, run the following commands in
a terminal (again, if you're on Windows, we recommend you use the _Git Bash_ that
ships with _Git_):

```bash
cd xai-demonstrator/deployments/test-local
docker-compose up
```

!!! warning "Download size"

    This will download several GB of files from the GitHub Container Registry!

!!! info "Permissions"

    Depending on your operating system and the precise configuration of your
    _Docker_ installation, you might need to execute `docker-compose up` with
    "super user" (MacOS and Linux) or "administrator" (Windows) privileges.   

After the downloads complete and the containers are spun up, you can visit your
very own _XAI Demonstrator_ at [http://localhost:8000/](http://localhost:8000/).

To launch this instance of the _XAI Demonstrator_, we used only a very small part
of the source code: The file [deployment/test-local/docker-compose.yml](https://github.com/XAI-Demonstrator/xai-demonstrator/deployment/test-local/docker-compose.yml).
It instructs the _Docker Engine_ to download and launch several containers
(four at the time of writing) that together comprise the _XAI Demonstrator_.

The `test-local` deployment configuration utilizes pre-built containers.
While this is great for quickly launching the _XAI Demonstrator_, if we
want to make changes to the code and test it, we need to build our own
containers from the source code stored locally on our computer.

As we'll see in the next section, this is not much more involved than
what we did so far. For now, terminate the _XAI Demonstrator_ instance.
In most terminals, this is accomplished by pressing <kbd>Ctrl</kbd> + <kbd>C</kbd>
(or <kbd>Cmd</kbd> + <kbd>C</kbd> on Macs).

## Run a single use case

The core components of the _XAI Demonstrator_ are its use cases.
Each use case illustrates and demonstrates an XAI concept or method.

By design, the use cases are self-contained. On the one hand, this gives
developers a lot of freedom in selecting, e.g., machine-learning
models and XAI libraries. On the other hand, it means that we can launch
a use case as a standalone instance.

To do this, navigate to a use case's main directory (in this guide, we'll
work with the _Visual Inspection_ use case):

```bash
cd xai-demonstrator/visual-inspection
```

Next, we will instruct _Docker_ to assemble a new container from the files 
in the current directory (`.`) and store it under the name `visual-inspection-service`:

```bash
docker build -t visual-inspection-service .
```

!!! warning "Download size"

    This will download potentially several GB of files from different package repositories!

While waiting for the command to complete, you can take a look at the
[`Dockerfile`](https://github.com/XAI-Demonstrator/xai-demonstrator/blob/master/visual-inspection/Dockerfile).
(We'll dive into the details of this file [later](use-cases.md), so don't
if at first sight it appears to be very complicated.)

When you scroll through the file, you can see that _Docker_ is instructed to `COPY`
source code from the `inspection-frontend` and `inspection-backend`. You might also
recognize some of the commands like `pip`, `npm`, or `apt-get` that are used to 
install the software dependencies required to run the use case.

Once `docker build` completes, you can launch the container:

```bash
docker run -p 8000:8000 visual-inspection-service
```

If you now visit [http://localhost:8000/](http://localhost:8000/), you will 
directly see the frontend for the _Visual Inspection_ use case. (You might
have to wait for a couple of seconds until the connection can be established.)

This instance of the use case should behave the same as the instance you launched
using the `test-local` deployment configuration: Both are based on the latest
version of the source code. The only difference is that instead of using a 
container that was built on _GitHub_, you built it yourself on your own computer.

Let's change that! Terminate the _Visual Inspection_ instance by pressing
<kbd>Ctrl</kbd> + <kbd>C</kbd> (or <kbd>Cmd</kbd> + <kbd>C</kbd> on Macs)
in the terminal.

## Modify a use case


## What's next?

Congratulations! You have not only set up everything that's necessary to run your very
own _XAI Demonstrator_, but already made changes to the source code of a use case and
tested the results. 

