from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Конфиг сервиса"""

    postgres_connection_string: str
    postgres_database_name: str
    postgres_host: str
    postgres_port: int
    postgres_username: str
    postgres_password: str

    @property
    def get_postgres_connecion_string(self):
        url = self.postgres_connection_string
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://") and "+asyncpg" not in url:
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return url
