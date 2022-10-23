import os
import subprocess
import sys
import traceback

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles

from app import models, views

app = FastAPI(openapi_url="/api/openapi.json", docs_url="/api/docs", redoc_url="/api/redoc")
os.makedirs('data', exist_ok=True)
models.init_db(app)


@app.on_event('startup')
async def startup():
    database = app.state.database
    if not database.is_connected:
        await database.connect()


@app.on_event('shutdown')
async def startup():
    database = app.state.database
    if database.is_connected:
        await database.disconnect()


# Add views in views/__init__.py or create routers in views/ and include them in this function
views.include_routers(app)


@app.middleware('http')
async def check_admin_ip(request: Request, call_next):
    # noinspection PyBroadException
    try:
        return await call_next(request)
    except Exception:
        return PlainTextResponse(traceback.format_exc(), status_code=500)


# Config CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

if not os.environ.get('DEBUG'):
    app.mount('/', StaticFiles(directory='public', html=True, check_dir=False), name='web')

if __name__ == '__main__':
    import uvicorn

    process = None

    if os.environ.get('DEBUG'):
        # Don't use shell=True on linux
        process = subprocess.Popen(['npm', 'run', 'dev'], shell=os.name == 'nt', cwd='web_src')
        args = {
            'reload': True,
            'port': 8080
        }
    else:
        if not getattr(sys, 'frozen', False):
            # Don't use shell=True on linux
            subprocess.Popen(['npm', 'run', 'build'], shell=os.name == 'nt', cwd='web_src').wait()

        args = {
            'workers': os.cpu_count(),
            'port': os.environ.get('WEB_PORT', 3000)  # Take over port 5000 from Vite
        }

    try:
        uvicorn.run('main:app', host='0.0.0.0', **args)
    finally:
        if process is not None:
            process.kill()
