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

    To install *Git*... 

!!! note "Downloading without Git"

    If you just want to quickly try out the _XAI Demonstrator_ and
    do not have Git installed, you can simply download the source code
    [as a ZIP file]().

    However, please note that without Git **you will not be able to
    build use cases containers yourself.** Thus, you are restricted to
    launching deployment configurations that utilize pre-built container
    images (more on that in the next section).

To download ("check out") the _XAI Demontrator_ source code from GitHub,
open a terminal (on Windows, we recommend *Git Bash*)
```bash
git clone https://github.com/xai-demonstrator/xai-demonstrator.git
```

After a couple of seconds, you'll find  the entire _XAI Demonstrator_ source
code in a new folder called `xai-demonstrator`.

## Install Docker



## Run your very own XAI Demonstrator instance


```bash
cd xai-demonstrator/deployments/test-local
docker-compose up
```

!!! warning "Download size"

    This will download several GB of files! 

We used only a small part of the source code:

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
