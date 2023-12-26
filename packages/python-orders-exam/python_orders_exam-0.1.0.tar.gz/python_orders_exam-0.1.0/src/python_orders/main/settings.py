from dataclasses import dataclass


class JSONSettings:
    orders_json_path: str


class SocketSettings:
    host: str
    port: int


class ServerSettings:
    json: JSONSettings
    socket: SocketSettings


class Settings:
    server: ServerSettings
