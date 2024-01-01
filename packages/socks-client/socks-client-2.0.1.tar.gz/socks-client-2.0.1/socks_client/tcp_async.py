import asyncio
import ipaddress
import socket

from ._errors import (SOCKS4_ERRORS, SOCKS5_ERRORS, GeneralProxyError,
                      ProxyError, SOCKS4Error, SOCKS5AuthError, SOCKS5Error)
from ._type import SOCKS4, SOCKS5


class socksocket:
    _socket = None

    def __init__(
        self,
        proxy_type,
        proxy_host: str,
        proxy_port: int,
        username=None,
        password=None,
        rdns=None,
        loop: asyncio.AbstractEventLoop = None,
    ):
        if loop is None:
            loop = asyncio.get_event_loop()
        self._loop = loop
        self._proxy_host = proxy_host
        self._proxy_port = proxy_port
        self._proxy_type = proxy_type
        self._username = username
        self._password = password
        self._rdns = rdns
        self._dest_host = None
        self._dest_port = None
        self._timeout = 60
        self._socket = None

    async def write_all(self, data):
        await self._loop.sock_sendall(self._socket, data)

    async def read(self, max_bytes=65536):
        return await self._loop.sock_recv(self._socket, max_bytes)

    async def read_exact(self, n):
        data = bytearray()
        while len(data) < n:
            packet = await self._loop.sock_recv(self._socket, n - len(data))
            if not packet:  # pragma: no cover
                raise ProxyError("Connection closed unexpectedly")
            data += packet
        return data

    async def close(self):
        if self._socket is not None:
            self._socket.close()

    async def connect(
        self, dest_host: str, dest_port: int, _socket=None
    ) -> socket.socket:
        self._dest_host = dest_host
        self._dest_port = dest_port
        self._socket = _socket
        try:
            return await self._connect()
        except asyncio.TimeoutError as e:
            raise GeneralProxyError("Proxy connection timed out", e)

    async def settimeout(self, timeout):
        self._timeout = timeout

    async def _connect(self) -> socket.socket:
        try:
            if self._socket is None:
                if isinstance(
                    ipaddress.ip_address(self._proxy_host), ipaddress.IPv4Address
                ):
                    self._socket = socket.socket(
                        family=socket.AF_INET, type=socket.SOCK_STREAM
                    )
                elif isinstance(
                    ipaddress.ip_address(self._proxy_host), ipaddress.IPv6Address
                ):
                    self._socket = socket.socket(
                        family=socket.AF_INET6, type=socket.SOCK_STREAM
                    )
                else:
                    raise
                self._socket.setblocking(False)
                address = (self._proxy_host, self._proxy_port)
                await self._loop.sock_connect(sock=self._socket, address=address)
            await self._negotiate()
            return self._socket
        except OSError as e:
            await self._close()
            # msg = "Could not connect to proxy {}:{} [{}]".format(self._proxy_host, self._proxy_port, e.strerror)
            raise e
        except asyncio.CancelledError as e:  # pragma: no cover
            await self._close()
            raise e
        except Exception as e:  # pragma: no cover
            await self._close()
            raise e

    async def _negotiate(self):
        if self._proxy_type == SOCKS5:
            await self._socks5_auth()
            await self._socks5_connect()
        elif self._proxy_type == SOCKS4:
            await self._socks4_connect()
        else:
            raise NotImplementedError()

    async def _close(self):
        if self:
            await self.close()

    async def _socks4_connect(self):
        if not self._rdns:
            family = socket.AF_UNSPEC
            infos = await self._loop.getaddrinfo(
                host=self._dest_host, port=0, family=family, type=socket.SOCK_STREAM
            )
            if not infos:  # pragma: no cover
                raise OSError(
                    "Can`t resolve address {}:{} [{}]".format(
                        self._dest_host, 0, family
                    )
                )
            infos = sorted(infos, key=lambda info: info[0])
            family, _, _, _, address = infos[0]
            _resolved_host = address[0]
        port_bytes = self._dest_port.to_bytes(2, "big")
        include_hostname = False
        # not IP address, probably a DNS name
        if self._rdns:
            # remote resolve (SOCKS4a)
            include_hostname = True
            host_bytes = bytes([0x00, 0x00, 0x00, 1])
        else:
            # resolve locally
            assert _resolved_host is not None
            addr = _resolved_host
            host_bytes = ipaddress.IPv4Address(addr).packed
        data = bytearray([0x04, 0x01])
        data += port_bytes
        data += host_bytes
        if self._username:
            data += self._username.encode("ascii")
        data.append(0x00)
        if include_hostname:
            data += self._dest_host.encode("idna")
            data.append(0x00)
        await self.write_all(data)
        chosen_r = await self.read_exact(8)
        chosen_res = chosen_r[:2]
        if chosen_res[0:1] != b"\x00":  # pragma: no cover
            raise SOCKS4Error("SOCKS4 proxy server sent invalid data")
        if chosen_res[1:2] != b"\x5A":  # pragma: no cover
            msg = SOCKS4_ERRORS.get(self.reply, "Unknown error")
            raise SOCKS4Error(msg, self.reply)

    async def _socks5_auth(self):
        auth_method = await self._choose_auth_method()
        if auth_method == 0x02:
            data = bytearray()
            data.append(0x01)
            data.append(len(self._username))
            data += self._username.encode("ascii")
            data.append(len(self._password))
            data += self._password.encode("ascii")
            await self.write_all(bytes(data))
            chosen_auth = await self.read_exact(2)
            if chosen_auth[0:1] != b"\x01":
                raise SOCKS5AuthError("Invalid authentication response")
            if chosen_auth[1:2] != b"\x00":
                raise SOCKS5AuthError("Username and password authentication failure")

    async def _choose_auth_method(self):
        if self._username and self._password:
            await self.write_all(b"\x05\x02\x00\x02")
        else:
            await self.write_all(b"\x05\x01\x00")
        chosen_auth = await self.read_exact(2)
        if chosen_auth[0:1] != b"\x05":
            raise ("SOCKS5 proxy server sent invalid data")
        if chosen_auth[1:2] == b"\x02":
            if not (self._username and self._password):
                raise (
                    "No username/password supplied. Server requested username/password authentication"
                )
        elif chosen_auth[1:2] != b"\x00":
            if chosen_auth[1:2] == b"\xFF":
                raise ("All offered SOCKS5 authentication methods were rejected")
            else:
                raise ("SOCKS5 proxy server sent invalid data")
        return chosen_auth[1]

    async def _socks5_connect(self):
        if not self._rdns:
            family = socket.AF_UNSPEC
            infos = await self._loop.getaddrinfo(
                host=self._dest_host, port=0, family=family, type=socket.SOCK_STREAM
            )
            if not infos:  # pragma: no cover
                raise OSError(
                    "Can`t resolve address {}:{} [{}]".format(
                        self._dest_host, 0, family
                    )
                )
            infos = sorted(infos, key=lambda info: info[0])
            family, _, _, _, address = infos[0]
            _resolved_host = address[0]
        data = bytearray([0x05, 0x01, 0x00])
        port = self._dest_port.to_bytes(2, "big")
        # not IP address, probably a DNS name
        if self._rdns:
            # resolve remotely
            address_type = 0x03
            host = self._dest_host.encode("idna")
            host_len = len(host)
            data += bytes([address_type, host_len]) + host + port
        else:
            assert _resolved_host is not None
            addr = _resolved_host
            ip = ipaddress.ip_address(addr)
            if ip.version == 4:
                address_type = 0x01
            elif ip.version == 6:
                address_type = 0x04
            else:
                raise ValueError("Invalid IP version")
            data += bytes([address_type]) + ip.packed + port
        await self.write_all(data)
        chosen_res = await self.read_exact(3)
        if chosen_res[0:1] != b"\x05":
            raise SOCKS5Error("Unexpected SOCKS version number")
        if chosen_res[1:2] != b"\x00":  # pragma: no cover
            msg = SOCKS5_ERRORS.get(self.reply, "Unknown error")
            raise SOCKS5Error(msg, self.reply)
        if chosen_res[2:3] != b"\x00":
            raise SOCKS5Error("The reserved byte must be {:#02X}".format(0x00))
        await self._read_bound_address()

    async def _read_bound_address(self):
        addr_type, *_ = await self.read_exact(1)
        if addr_type == 0x01:
            host = await self.read_exact(4)
            host = socket.inet_ntop(socket.AF_INET, host)
        elif addr_type == 0x04:
            host = await self.read_exact(16)
            host = socket.inet_ntop(socket.AF_INET6, host)
        elif addr_type == 0x03:  # pragma: no cover
            host_len, *_ = await self.read_exact(1)
            host = await self.read_exact(host_len)
            host = host.decode()
        else:  # pragma: no cover
            raise GeneralProxyError("Invalid address type: {:#02X}".format(addr_type))
        port = await self.read_exact(2)
        port = int.from_bytes(port, "big")
        return host, port
