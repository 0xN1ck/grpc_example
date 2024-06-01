from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_HOST_LOCAL: str = '0.0.0.0'
    SERVICE_PORT: int = 8080

    GRPC_HOST_LOCAL: str = '0.0.0.0'
    GRPC_PORT: int = 50091


settings = Settings()
