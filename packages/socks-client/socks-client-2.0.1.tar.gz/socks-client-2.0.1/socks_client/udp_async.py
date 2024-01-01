import socket
import struct
from errno import EAGAIN, EINVAL, EOPNOTSUPP
from io import BytesIO
from os import SEEK_CUR

from ._errors import (SOCKS5_ERRORS, GeneralProxyError, SOCKS5AuthError,
                      SOCKS5Error)
from ._type import SOCKS5

_orig_socket = socket.socket


async def set_default_proxy(
    proxy_type=None, addr=None, port=None, rdns=True, username=None, password=None
):
    """Sets a default proxy.

    All further socksocket objects will use the default unless explicitly
    changed. All parameters are as for socket.set_proxy()."""
    socksocket.default_proxy = (
        proxy_type,
        addr,
        port,
        rdns,
        username.encode() if username else None,
        password.encode() if password else None,
    )


async def setdefaultproxy(*args, **kwargs):
    if "proxytype" in kwargs:
        kwargs["proxy_type"] = kwargs.pop("proxytype")
    return await set_default_proxy(*args, **kwargs)


class socksocket(socket.socket):
    """socksocket([family[, type[, proto]]]) -> socket object

    Open a SOCKS enabled socket. The parameters are the same as
    those of the standard socket init. In order for SOCKS to work,
    you must specify family=AF_INET and proto=0.
    The "type" argument must be either SOCK_STREAM or SOCK_DGRAM.
    """

    default_proxy = None

    def __init__(
        self, family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, *args, **kwargs
    ):
        if type not in (socket.SOCK_STREAM, socket.SOCK_DGRAM):
            msg = "Socket type must be stream or datagram, not {!r}"
            raise ValueError(msg.format(type))
        super(socksocket, self).__init__(family, type, proto, *args, **kwargs)
        self._proxyconn = None  # TCP connection to keep UDP relay alive
        if self.default_proxy:
            self.proxy = self.default_proxy
        else:
            self.proxy = (None, None, None, None, None, None)
        self.proxy_sockname = None
        self.proxy_peername = None
        self._timeout = None

    async def _readall(self, file, count):
        """Receive EXACTLY the number of bytes requested from the file object.
        Blocks until the required number of bytes have been received."""
        data = b""
        while len(data) < count:
            d = file.read(count - len(data))
            if not d:
                raise GeneralProxyError("Connection closed unexpectedly")
            data += d
        return data

    async def settimeout(self, timeout):
        self._timeout = timeout
        try:
            # test if we're connected, if so apply timeout
            # peer = self.get_proxy_peername()
            super(socksocket, self).settimeout(self._timeout)
        except socket.error:
            pass

    async def bind(self, *pos, **kw):
        """Implements proxy connection for UDP sockets.
        Happens during the bind() phase."""
        (proxy_type, proxy_addr, proxy_port, rdns, username, password) = self.proxy
        if not proxy_type or self.type != socket.SOCK_DGRAM:
            return _orig_socket.bind(self, *pos, **kw)
        if self._proxyconn:
            raise socket.error(EINVAL, "Socket already bound to an address")
        if proxy_type != SOCKS5:
            msg = "UDP only supported by SOCKS5 proxy type"
            raise socket.error(EOPNOTSUPP, msg)
        super(socksocket, self).bind(*pos, **kw)
        # Need to specify actual local port because
        # some relays drop packets if a port of zero is specified.
        # Avoid specifying host address in case of NAT though.
        _, port = self.getsockname()
        dst = ("0", port)
        self._proxyconn = _orig_socket()
        proxy = await self._proxy_addr()
        self._proxyconn.connect(proxy)
        UDP_ASSOCIATE = b"\x03"
        _, relay = await self._SOCKS5_request(self._proxyconn, UDP_ASSOCIATE, dst)
        # The relay is most likely on the same host as the SOCKS proxy,
        # but some proxies return a private IP address (10.x.y.z)
        host, _ = proxy
        _, port = relay
        super(socksocket, self).connect((host, port))
        super(socksocket, self).settimeout(self._timeout)
        self.proxy_sockname = ("0.0.0.0", 0)  # Unknown

    async def sendto(self, bytes, *args, **kwargs):
        if self.type != socket.SOCK_DGRAM:
            return super(socksocket, self).sendto(bytes, *args, **kwargs)
        if not self._proxyconn:
            await self.bind(("", 0))
        address = args[-1]
        flags = args[:-1]
        header = BytesIO()
        RSV = b"\x00\x00"
        header.write(RSV)
        STANDALONE = b"\x00"
        header.write(STANDALONE)
        await self._write_SOCKS5_address(address, header)
        sent = super(socksocket, self).send(header.getvalue() + bytes, *flags, **kwargs)
        return sent - header.tell()

    async def recvfrom(self, bufsize, flags=0):
        if self.type != socket.SOCK_DGRAM:
            return super(socksocket, self).recvfrom(bufsize, flags)
        if not self._proxyconn:
            await self.bind(("", 0))
        buf = BytesIO(super(socksocket, self).recv(bufsize + 1024, flags))
        buf.seek(2, SEEK_CUR)
        frag = buf.read(1)
        if ord(frag):
            raise NotImplementedError("Received UDP packet fragment")
        fromhost, fromport = await self._read_SOCKS5_address(buf)
        if self.proxy_peername:
            peerhost, peerport = self.proxy_peername
            if fromhost != peerhost or peerport not in (0, fromport):
                raise socket.error(EAGAIN, "Packet filtered")
        return (buf.read(bufsize), (fromhost, fromport))

    async def close(self):
        if self._proxyconn:
            self._proxyconn.close()
        return super(socksocket, self).close()

    async def _negotiate_SOCKS5(self, *dest_addr):
        """Negotiates a stream connection through a SOCKS5 server."""
        CONNECT = b"\x01"
        self.proxy_peername, self.proxy_sockname = await self._SOCKS5_request(
            self, CONNECT, dest_addr
        )

    async def _SOCKS5_request(self, conn, cmd, dst):
        """
        Send SOCKS5 request with given command (CMD field) and
        address (DST field). Returns resolved DST address that was used.
        """
        proxy_type, addr, port, rdns, username, password = self.proxy
        writer = conn.makefile("wb")
        reader = conn.makefile("rb", 0)  # buffering=0 renamed in Python 3
        try:
            # First we'll send the authentication packages we support.
            if username and password:
                # The username/password details were supplied to the
                # set_proxy method so we support the USERNAME/PASSWORD
                # authentication (in addition to the standard none).
                writer.write(b"\x05\x02\x00\x02")
            else:
                # No username/password were entered, therefore we
                # only support connections with no authentication.
                writer.write(b"\x05\x01\x00")
            # We'll receive the server's response to determine which
            # method was selected
            writer.flush()
            chosen_auth = await self._readall(reader, 2)
            if chosen_auth[0:1] != b"\x05":
                # Note: string[i:i+1] is used because indexing of a bytestring
                # via bytestring[i] yields an integer in Python 3
                raise GeneralProxyError("SOCKS5 proxy server sent invalid data")
            # Check the chosen authentication method
            if chosen_auth[1:2] == b"\x02":
                # Okay, we need to perform a basic username/password
                # authentication.
                if not (username and password):
                    # Although we said we don't support authentication, the
                    # server may still request basic username/password
                    # authentication
                    raise SOCKS5AuthError(
                        "No username/password supplied. Server requested username/password authentication"
                    )
                writer.write(
                    b"\x01"
                    + chr(len(username)).encode()
                    + username
                    + chr(len(password)).encode()
                    + password
                )
                writer.flush()
                auth_status = await self._readall(reader, 2)
                if auth_status[0:1] != b"\x01":
                    # Bad response
                    raise GeneralProxyError("SOCKS5 proxy server sent invalid data")
                if auth_status[1:2] != b"\x00":
                    # Authentication failed
                    raise SOCKS5AuthError("SOCKS5 authentication failed")
                # Otherwise, authentication succeeded
            # No authentication is required if 0x00
            elif chosen_auth[1:2] != b"\x00":
                # Reaching here is always bad
                if chosen_auth[1:2] == b"\xFF":
                    raise SOCKS5AuthError(
                        "All offered SOCKS5 authentication methods were rejected"
                    )
                else:
                    raise GeneralProxyError("SOCKS5 proxy server sent invalid data")
            # Now we can request the actual connection
            writer.write(b"\x05" + cmd + b"\x00")
            resolved = await self._write_SOCKS5_address(dst, writer)
            writer.flush()
            # Get the response
            resp = await self._readall(reader, 3)
            if resp[0:1] != b"\x05":
                raise GeneralProxyError("SOCKS5 proxy server sent invalid data")
            status = ord(resp[1:2])
            if status != 0x00:
                # Connection failed: server returned an error
                error = SOCKS5_ERRORS.get(status, "Unknown error")
                raise SOCKS5Error("{:#04x}: {}".format(status, error))
            # Get the bound address/port
            bnd = await self._read_SOCKS5_address(reader)
            super(socksocket, self).settimeout(self._timeout)
            return (resolved, bnd)
        finally:
            reader.close()
            writer.close()

    async def _write_SOCKS5_address(self, addr, file):
        """
        Return the host and port packed for the SOCKS5 protocol,
        and the resolved address as a tuple object.
        """
        host, port = addr
        proxy_type, _, _, rdns, username, password = self.proxy
        family_to_byte = {socket.AF_INET: b"\x01", socket.AF_INET6: b"\x04"}
        # If the given destination address is an IP address, we'll
        # use the IP address request even if remote resolving was specified.
        # Detect whether the address is IPv4/6 directly.
        for family in (socket.AF_INET, socket.AF_INET6):
            try:
                addr_bytes = socket.inet_pton(family, host)
                file.write(family_to_byte[family] + addr_bytes)
                host = socket.inet_ntop(family, addr_bytes)
                file.write(struct.pack(">H", port))
                return host, port
            except socket.error:
                continue
        # Well it's not an IP number, so it's probably a DNS name.
        if rdns:
            # Resolve remotely
            host_bytes = host.encode("idna")
            file.write(b"\x03" + chr(len(host_bytes)).encode() + host_bytes)
        else:
            # Resolve locally
            addresses = socket.getaddrinfo(
                host,
                port,
                socket.AF_UNSPEC,
                socket.SOCK_STREAM,
                socket.IPPROTO_TCP,
                socket.AI_ADDRCONFIG,
            )
            # We can't really work out what IP is reachable, so just pick the
            # first.
            target_addr = addresses[0]
            family = target_addr[0]
            host = target_addr[4][0]
            addr_bytes = socket.inet_pton(family, host)
            file.write(family_to_byte[family] + addr_bytes)
            host = socket.inet_ntop(family, addr_bytes)
        file.write(struct.pack(">H", port))
        return host, port

    async def _read_SOCKS5_address(self, file):
        atyp = await self._readall(file, 1)
        if atyp == b"\x01":
            addr = socket.inet_ntoa(await self._readall(file, 4))
        elif atyp == b"\x03":
            length = await self._readall(file, 1)
            addr = await self._readall(file, ord(length))
        elif atyp == b"\x04":
            addr = socket.inet_ntop(socket.AF_INET6, await self._readall(file, 16))
        else:
            raise GeneralProxyError("SOCKS5 proxy server sent invalid data")
        port = struct.unpack(">H", await self._readall(file, 2))[0]
        return addr, port

    _proxy_negotiators = {SOCKS5: _negotiate_SOCKS5}

    async def _proxy_addr(self):
        """
        Return proxy address to connect to as tuple object
        """
        (proxy_type, proxy_addr, proxy_port, rdns, username, password) = self.proxy
        proxy_port = proxy_port or 1080
        if not proxy_port:
            raise GeneralProxyError("Invalid proxy type")
        return proxy_addr, proxy_port
