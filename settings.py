from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_HOST_LOCAL: str = '0.0.0.0'
    SERVICE_PORT: int = 1111

    GRPC_HOST_LOCAL: str = '0.0.0.0'
    GRPC_PORT: int = 50091

    JAEGER_HOST: str = "0.0.0.0"
    JAEGER_PORT: int = 14250

    SECRET_KEY: str = 'secret_key'


settings = Settings()
