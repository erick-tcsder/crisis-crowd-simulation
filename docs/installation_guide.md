# Guía de instalación

## Frontend
Para instalar el software de Frontend:
1. Instalar nvm (omitir si ya está instalado)
   - Guía para [Windows](https://www.freecodecamp.org/news/nvm-for-windows-how-to-download-and-install-node-version-manager-in-windows-10/)
   - Guía para [Unix/MacOS](https://github.com/nvm-sh/nvm#installing-and-updating)
2. Instala la versión correcta de NodeJS:
  ```bash
  nvm install 18.12.1
  ```
3. Instala dependencias e inicia el proyecto:
   ```shell
   npm install
   npm start
   ```

## Backend:
Para instalar el software de Backend:
1. Instalar version de Python `3.10.4`
2. Crear *virtual environment* e instalar dependencias:
   ```bash
   $ > cd ./backend
   $./backend > python --version
   #should be 3.10.3
   $./backend > python -m venv venv
   #venv activation run activate script depending your shell
   (venv)$./backend > python -m pip install -r requirement.txt
   ```
3. Iniciar servidor:
   ```bash
   (venv)$./backend > uvicorn main:app
   ```