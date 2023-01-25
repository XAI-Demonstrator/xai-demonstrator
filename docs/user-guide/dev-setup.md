# Set Up Your Development Environment

The purpose of this short instruction is to set up an environment to clone the repository and run it locally on the users computer. 

!!! note "Quick start for advanced developers"

    If you've developed software using (parts of) the XAI Demonstrator's [tech stack](/tech-notes/tech-stack/) before,
    chances are that you already have the required software installed or do not need detailed setup instructions.

    To write code for the XAI Demonstrator, you need

    - Git
    - Node.js
    - Python

    Then, you can clone
    [github.com/XAI-Demonstrator/xai-demonstrator](https://github.com/XAI-Demonstrator/xai-demonstrator)
    and are good to go.

## Tools

All you need is a text editor and a terminal
(under Windows, we recommend you use *Git Bash* that ships with [Git for Windows](https://gitforwindows.org/)).

The XAI Demonstrator team uses *PyCharm Professional*, which supports not only Python, but web development as well.
It can be downloaded [here](https://www.jetbrains.com/de-de/pycharm/download/).
(Note that the *Community* version has only limited support for web development.
The *Professional* version can be obtained for free for students and other educational users.)

## Get the code

### Install Git

As is the case for almost all modern software projects,
the _XAI Demonstrator_'s code is stored in a [Git](https://git-scm.com/) repository.

!!! note "Prepare your macOS device 🍎"

    If your computer is running macOS, it's easiest to use Homebrew to install Git and the other required software.

    If Homebrew ist not yet installed, run following command in the command line:  

    `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

- **macOS**: `brew install git`
- **Linux (Debian-based)**: `apt-get install git`
- **Windows**: Download installer from [the official website](https://git-scm.com/download/win)

### Clone the repository

Navigate to the directory in which you want to keep the source code and run

```shell
git clone https://github.com/XAI-Demonstrator/xai-demonstrator.git
```

## Prepare for frontend development

### Install Node.js
The _XAI Demonstrator_'s frontends require the [Node.js JavaScript runtime](https://nodejs.org/en/) version 14.

- **macOS**: `brew install node@14`
- **Windows**: Download the installer from [the official website](https://nodejs.org/dist/latest-v14.x/ )

!!! note "Recommendation: Use a Node.js Version Manager 💡"

    If you frequently work with Node.js or would like to install Node.js cleanly separated from your other
    software, we recommend you use a version manager such as [NVM](https://github.com/nvm-sh/nvm)
    or [NVM for Windows](https://github.com/coreybutler/nvm-windows)

### Install frontend dependencies

Navigate to the frontend's directory (e.g., `cd visual-inspection/inspection-frontend`)
and run `npm install`.

To check that everything works as expected, run `npm run test:unit` to execute the unit test suite.

Afterwards, you can launch the frontend development server using `npm run serve`.

## Prepare for backend development

### Install Python

The _XAI Demonstrator_'s backends require Python 3.8.
We recommend that you set up a dedicated Python environment for your work on the XAI Demonstrator.
While the different components and use cases each have their own set of requirements, to date these requirements are compatible.

- **Linux**: We recommend using [PyEnv](https://github.com/pyenv/pyenv) to obtain the correct Python version and set up the virtual environment.
- **macOS and Windows**: We recommend using the [Anaconda distribution](https://www.anaconda.com/products/individual).

### Install backend dependencies

Make sure your Python environment is activated
and navigate to the backend's directory (e.g., `cd visual-inspection/inspection-backend`).

Then, first run `pip install -r requirements.txt` to install the backend's dependencies.
To install the test dependencies that are only required for testing and development purposes,
run `pip install -r requirements-test.txt`.

Next, run the following command to download the machine-learning model for the use case:
`./download_models.sh my_model`.

To check that everything works as expected, run `pytest tests/` to execute the unit test suite.

## What's next?

*TODO*
