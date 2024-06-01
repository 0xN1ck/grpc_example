import asyncio
import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from grpc_core.servers.manager import Server

from settings import settings
from api import order


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(Server().run())
    try:
        yield
    finally:
        await Server().stop()


app = FastAPI(
    lifespan=lifespan,
    title='Example gRPC service on Python',
    description='This showing how to use gRPC on Python',
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(order.router)

if __name__ == '__main__':
    uvicorn.run('main:app', port=settings.SERVICE_PORT, host=settings.SERVICE_HOST_LOCAL, reload=True)
