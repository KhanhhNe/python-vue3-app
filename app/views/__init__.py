from fastapi import APIRouter, FastAPI


main_router = APIRouter()


@main_router.get('/hello')
def index():
    return {'message': 'Hello World'}


def include_routers(app: FastAPI):
    app.include_router(main_router, prefix='/api')
