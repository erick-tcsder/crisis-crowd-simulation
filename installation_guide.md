# Installation Guide

## Setup Frontend App
1. Install nvm (omit if you alredy have it)
   - Installation guide for [Windows](https://www.freecodecamp.org/news/nvm-for-windows-how-to-download-and-install-node-version-manager-in-windows-10/)
   - Installation Guide for [Unix/MacOS](https://github.com/nvm-sh/nvm#installing-and-updating)
2. Install the right version of NodeJS:
  ```bash
  nvm install 18.12.1
  ```
3. Install Dependecies and start the Project:
   ```shell
   npm install
   npm start
   ```

## Setup Core and Backend App:
1. Install python version `3.10.4`
2. Create a virtual enviroment and install dependencies:
   ```bash
   $ > cd ./backend
   $./backend > python --version
   #should be 3.10.3
   $./backend > python -m venv venv
   #venv activation run activate script depending your shell
   (venv)$./backend > python -m pip install -r requirement.txt
   ```
3. Run server:
   ```bash
   (venv)$./backend > uvicorn main:app
   ```