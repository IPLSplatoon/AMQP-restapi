from fastapi import FastAPI
from restapi.rpc import Client


class CustomFastAPI(FastAPI):
    """
    Custom FastAPI Class
    """

    rpc_client: Client
