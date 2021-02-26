# Permanent deployment


## What does 'deployment' mean?

In the
[Getting Started](getting_started.md#run-your-very-own-xai-demonstrator-instance)
chapter of this user guide, you have learned how to spin up an XAI Demonstrator instance.

In IT lingo, a 'deployment' is a permanently running instance of an IT system.
It comprises both a number of services, their configuration, and the infrastructure on which it runs.

## Deploy a private instance in a private network

You can use the 
[_test-local_](https://github.com/XAI-Demonstrator/xai-demonstrator/tree/master/deployment/test-local)
configuration as described in 
[Getting Started](getting_started.md#run-your-very-own-xai-demonstrator-instance).

If you want to use your own or modified use cases, there are two options.

If have your own container registry, which we recommend, you can fork
[_test-local_](https://github.com/XAI-Demonstrator/xai-demonstrator/tree/master/deployment/test-local).

If you don't, you will need to build the containers on the target machine.

Check out the ["global" _docker-compose.yml_](https://github.com/XAI-Demonstrator/xai-demonstrator/blob/master/docker-compose.yml)
and work from there.

!!! note "Ports"

    For others to access your deployment, you need to open the port your server is running at.

    In the standard configuration, that's port 8000.

## Deploy a public instance on the internet

You probably want to have HTTPS and run on a dedicated server.
Never connect your personal computers or internal servers to the internet!

We strongly recommend using a dedicated VM instance.

!!! note "Ports"

    For others to access your deployment, you need to open ports 80 and 443.

## Deploy a production-grade setup on Google Cloud Platform

What is the difference?

!!! warning "Costs"

    You need to set spending limits and monitor the costs.

## What's next?
