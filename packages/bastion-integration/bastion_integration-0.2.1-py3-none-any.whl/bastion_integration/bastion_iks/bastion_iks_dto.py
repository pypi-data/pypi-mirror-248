
from pydantic import BaseModel


class OperatorInfo(BaseModel):
    login: str
    password: str


class ServerConfig(BaseModel):
    host: str
    port: int
    certificate: str = ""
    https: bool = False


class BastionV2Config(BaseModel):
    server_config: ServerConfig
    operator_info: OperatorInfo
    enable_integration: bool = False
