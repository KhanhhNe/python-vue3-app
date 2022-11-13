import os
import traceback
from functools import cache
from typing import Any, Dict

import docstring_parser
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles

from app import models, views


class CustomFastAPI(FastAPI):
    @cache
    def openapi(self) -> Dict[str, Any]:
        schema = super().openapi().copy()

        for path, methods in schema['paths'].items():
            for method, data in methods.items():
                description = data.get('description', '')
                parsed = docstring_parser.parse(description)

                description = parsed.short_description

                # Add Markdown-formatted information (params, raises, returns) to the description
                if parsed.params:
                    params = [
                        f"- {param.arg_name}: {param.description}" for param in parsed.params
                    ]
                    description += f"\n\n### Parameters\n" + '\n'.join(params)

                if parsed.raises:
                    raises = [
                        f"- {raise_.type_name}: {raise_.description}" for raise_ in parsed.raises
                    ]
                    description += f"\n\n### Raises\n" + '\n'.join(raises)

                if parsed.returns:
                    description += f"\n\n### Returns\n" + f"- {parsed.returns.description}"

                data['description'] = description

        return schema


app = CustomFastAPI(
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
