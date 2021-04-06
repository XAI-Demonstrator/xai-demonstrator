# Set Up Your Development Environment

The purpose of this short instruction is to set up an environment to clone the repository and run it locally on the users computer. 

## Quick Start

If you've developed with (parts of) the XAI Demonstrator's [tech stack](/tech-notes/tech-stack.md) before,
chances are that you already have the required software installed or do not need detailed installation instructions.

To write code for the XAI Demonstrator, you need
- Git
- NodeJS
- Python

Then, you can clone
[github.com/XAI-Demonstrator/xai-demonstrator](https://github.com/XAI-Demonstrator/xai-demonstrator)
and are good to go.

## Install Git

As almost all modern software projects, the XAI Demonstrator's code is stored in a [Git](https://git-scm.com/) repository.

!!! note "Prepare your macOS device 🍎"

    If your computer is running macOS, it's easiest to use Homebrew to install Git and the other required software.

    If Homebrew ist not yet installed, run following command in the command line:  

    `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`


- **macOS**: `brew install git`
- **Linux (Debian-based)**: `apt-get install git`
- **Windows**: Download installer from [the official website](https://git-scm.com/download/win)

## Install NodeJS

The XAI Demonstrator's frontend requires the [NodeJS JavaScript runtime](https://nodejs.org/en/).

- **macOS**: `brew install node@12`
- **Windows**: Download the installer from [the official website](https://nodejs.org/dist/latest-v12.x/ )

!!! note "Recommendation: Use a Node Version Manager 💡"

    If you frequently work with NodeJS or would like to install NodeJS cleanly separated from your other
    software, we recommend you use a version manager such as [NVM](https://github.com/nvm-sh/nvm)
    or [NVM for Windows](https://github.com/coreybutler/nvm-windows)

## Install Python

The XAI Demonstrator requires Python 3.8.
We recommend that you set up a dedicated Python environment for your work on the XAI Demonstrator.
While the different components and use cases each have their own set of requirements, to date these requirements are compatible.

- **Linux**: We recommend using [PyEnv](https://github.com/pyenv/pyenv) to obtain the correct Python version and set up the virtual environment.
- **macOS and Windows**: We recommend using the [Anaconda distribution](https://www.anaconda.com/products/individual).


## Tools

PyCharm Professional can be downloaded under following link: 

- https://www.jetbrains.com/de-de/pycharm/download/


### Set up local server 

Navigate in: 

- visual-inspection/inspection-frontend/
 
Now install npm:

- npm install 

Run npm: 

- npm run serve

Now click on one of the links to run the visual inspection use case locally.