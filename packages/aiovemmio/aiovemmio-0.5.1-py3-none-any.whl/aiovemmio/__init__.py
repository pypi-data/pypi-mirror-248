import base64
from typing import Any, Self, Iterable

import aiohttp
import asyncio

CONNECT_ERRORS = (
    aiohttp.ClientError,
    asyncio.TimeoutError,
    OSError,
)


class DeviceInfo:
    def __init__(self, mac, type, revision):
        self.mac = mac
        self.type = type
        self.revision = revision

    @classmethod
    def from_dict(cls, json: dict[str, Any]) -> Self:
        return cls(
            json["mac"],
            json["type"],
            json["revision"],
        )


class DeviceNode:
    def __init__(self, uuid: bytes, capabilities: Iterable[str]):
        self.uuid = uuid
        self.capabilities = capabilities

    @classmethod
    def from_dict(cls, json: dict[str, Any]) -> Self:
        return cls(
            base64.b64decode(json["UUID"]),
            json["Capabilities"],
        )


class DeviceConnectionError(Exception):
    pass


class Client:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def get_info(self, session: aiohttp.ClientSession) -> DeviceInfo:
        try:
            async with session.get(
                f"http://{self.host}:{self.port}/api/v1/settings/structure",
                raise_for_status=True,
                timeout=10,
            ) as resp:
                return DeviceInfo.from_dict(await resp.json())
        except CONNECT_ERRORS as err:
            raise DeviceConnectionError(err) from err

    async def get_nodes(self, session: aiohttp.ClientSession) -> Iterable[DeviceNode]:
        try:
            async with session.get(
                f"http://{self.host}:{self.port}/api/v1/settings/nodes",
                raise_for_status=True,
                timeout=10,
            ) as resp:
                json = await resp.json()
                return [DeviceNode.from_dict(c) for c in json["Capabilities"]]
        except CONNECT_ERRORS as err:
            raise DeviceConnectionError(err) from err
