import os
import sys
import traceback

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles

from app import models, views

app = FastAPI(
    title="Python Vue3 App",
    version="0.0.1",
    openapi_url="/api/openapi.json", docs_url="/api/docs", redoc_url="/api/redoc"
)
os.makedirs('data', exist_ok=True)
os.environ['PATH'] = os.path.abspath('executables') + os.pathsep + os.environ['PATH']
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
async def return_exception_message(request: Request, call_next):
    # noinspection PyBroadException
    try:
        return await call_next(request)
    except Exception:
        traceback.print_exc()
        return PlainTextResponse(traceback.format_exc(), status_code=500)


# Config CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

if not os.environ.get('DEBUG'):
    public_dir = 'public'
    app.mount('/', StaticFiles(directory=public_dir, html=True, check_dir=False), name='public')
