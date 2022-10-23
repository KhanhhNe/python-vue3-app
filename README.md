# Python Vue 3 App Template

This is a template for a Python Vue 3 app. It uses [Pipenv](https://pipenv.pypa.io/en/latest/) for python dependencies
and [Vite](https://vitejs.dev/) for Vue 3 development. For Backend, it uses [FastAPI](https://fastapi.tiangolo.com/).
For Frontend, it uses [Vue 3](https://v3.vuejs.org/) with [TailwindCSS](https://tailwindcss.com/)
and [TypeScript](https://www.typescriptlang.org/).

## Getting Started

### Prerequisites

- [Python](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/en/)

### Installing

1. Clone the repo

    ```sh
    git clone https://github.com/KhanhhNe/python-vue3-app.git
    ```

2. Install Python dependencies

   ```sh
   pipenv install
   ```

3. Install Node.js dependencies

   ```sh
   cd web_src/
   npm install
   ```

4. Run the app

   Run in production mode (no Vue or FastAPI auto-reload)

   ```sh
   pipenv run main.py
   ```

   Run in development mode (with Vue and FastAPI auto-reload)

   ```sh
   export DEBUG=1 && pipenv run main.py
   ```

   Or on Windows

   ```sh
   set DEBUG=1 ; pipenv run main.py
   ```

## Notes

1. How the template works
    - The `web_src/` directory is the root directory for the `Vue` app. It is mounted at `/` in the `FastAPI` app when running in production mode.
    - When in development mode, the `Vue` app is served by `Vite` and the `FastAPI` app is served by `Uvicorn`. The `Vue` app is mounted at `/` and the `FastAPI` app is mounted at `/api/`. In this mode, `FastAPI` must be running on port 8080 so that `Vite` server could proxy the requests to it.

2. Where to add things
    - The Vue 3 app title will be set to the `FastAPI` title (you can change this in `main.py`). The FastAPI server also exposes useful OpenAPI urls (e.g. `/api/docs`, `/api/redoc`, `/api/openapi.json`) that you can use in the Vue app.
    - `FastAPI` routers should be added in `views/` folder, since `FastAPI` requires a specific order of routers, middlewares, and dependencies to work properly, so only change them if you know what you are doing.
    - There are an empty `typings.d.ts` file in `web_src/src/` directory. You can add your own `Typescript` typings here.
