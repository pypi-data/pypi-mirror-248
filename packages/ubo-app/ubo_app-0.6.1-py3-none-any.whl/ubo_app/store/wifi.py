# ruff: noqa: D100, D101, D102, D103, D104, D107
from __future__ import annotations

from enum import Enum

from redux import BaseAction, BaseEvent, Immutable


class WiFiType(str, Enum):
    WEP = 'WEP'
    WPA = 'WPA'
    WPA2 = 'WPA2'
    nopass = 'NOPASS'


class WiFiConnection(Immutable):
    ssid: str
    is_active: bool = False
    signal_strength: int = 0
    password: str | None = None
    type: WiFiType | None = None
    hidden: bool = False


class WiFiAction(BaseAction):
    ...


class WiFiUpdateActionPayload(Immutable):
    connections: list[WiFiConnection]
    is_on: bool
    current_connection: WiFiConnection | None


class WiFiUpdateAction(WiFiAction):
    payload: WiFiUpdateActionPayload


class WiFiUpdateRequestActionPayload(Immutable):
    reset: bool = False


class WiFiUpdateRequestAction(WiFiAction):
    payload: WiFiUpdateRequestActionPayload = WiFiUpdateRequestActionPayload(
        reset=False,
    )


class WiFiState(Immutable):
    connections: list[WiFiConnection] | None
    is_on: bool
    current_connection: WiFiConnection | None


class WiFiEvent(BaseEvent):
    ...


class WiFiCreateEventPayload(Immutable):
    connection: WiFiConnection


class WiFiCreateEvent(WiFiEvent):
    payload: WiFiCreateEventPayload


class WiFiUpdateRequestEvent(WiFiEvent):
    payload: None = None
