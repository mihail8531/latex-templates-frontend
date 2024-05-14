from httpx import AsyncClient


class BackendService:
    def __init__(self, http_client: AsyncClient) -> None:
        self.client = http_client
    
    async def login()
    
