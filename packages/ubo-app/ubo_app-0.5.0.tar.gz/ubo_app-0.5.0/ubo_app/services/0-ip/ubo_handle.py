# ruff: noqa: D100, D101, D102, D103, D104, D107, N999
from __future__ import annotations

import psutil
from reducer import reducer
from setup import init_service

from ubo_app.load_services import register_service

register_service(
    service_id='ip',
    label='IP',
    reducer=reducer,
)

init_service()


def get_ip_addresses():
    ip_addresses = {}
    for interface_name, interface_addresses in psutil.net_if_addrs().items():
        for address in interface_addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                ip_addresses[interface_name] = address.address
    return ip_addresses


ips = get_ip_addresses()
for interface, ip in ips.items():
    print(f'{interface}: {ip}')
