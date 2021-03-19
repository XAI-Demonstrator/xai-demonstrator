# Installation

The purpose of this short instruction is to set up a environment to clone the repository and run it locally on the users computer. 

First of all the user needs Git. If Homebrew ist not yet installed run following command in the command line:  

- /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

### Install Git:  

- brew install git 

To be able to retrieve data from our repository hosted on GitHub we use pycharm professional. Pycharm professional can be 
downloaded under following link: 

- https://www.jetbrains.com/de-de/pycharm/download/

### Clone repository

Open the repository on Github: 

- https://github.com/XAI-Demonstrator/xai-demonstrator

Copy link under code button and navigate in terminal to desired folder to save the project. Then run: 

- git clone „fill in github link“

### Install Node package 

To install the package run following command in command line: 

- brew install node@12

OR open

- https://nodejs.org/dist/latest-v12.x/ 
  
and run the suitable .msi file 

### Set up local server 

Navigate in: 

- visual-inspection/inspection-frontend/
 
Now install npm:

- npm install 

Run npm: 

- npm run serve

Now click on one of the links to run the visual inspection use case locally.