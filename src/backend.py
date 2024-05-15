from httpx import AsyncClient
from fastapi import status
from warnings import warn


class BackendError(BaseException):
    pass


class InvalidCredentialsError(BackendError):
    pass

class NotAuthorizedError(BackendError): 
    pass

class BackendService:
    def __init__(self, http_client: AsyncClient) -> None:
        self.client = http_client

    async def login(self, username: str, password: str) -> str:
        response = await self.client.post(
            "/auth/token", data={"username": username, "password": password}
        )
        warn(response.content)
        if response.status_code == status.HTTP_200_OK:
            return response.json()["access_token"]
        raise InvalidCredentialsError()
    
    async def check_logged(self) -> None:
        response = await self.client.get("/user/me")
        warn(response.status_code)
        if response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN):

            raise NotAuthorizedError()
        

