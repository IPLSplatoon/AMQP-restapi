import uvicorn
from contextlib import asynccontextmanager
import os

from restapi.CustomFastAPI import CustomFastAPI
from restapi.rpc import Client
from restapi.routes import rpc_router

rpc_uri = os.getenv("RPC_URI")
if not rpc_uri:
    raise ValueError("RPC_URI environment variable is not set.")


# Startup & Shutdown functions
@asynccontextmanager
async def lifespan(app: CustomFastAPI):
    await app.rpc_client.connect()
    yield  # Run the application


def create_app():
    new_app = CustomFastAPI(title="AMPQ Debugger API", redoc_url="/docs", docs_url=None, lifespan=lifespan)

    new_app.rpc_client = Client(
        uri=rpc_uri,
    )

    new_app.include_router(
        rpc_router,
        prefix="/rpc",
        tags=["RPC"],
    )

    return new_app


app = create_app()
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=2000)
