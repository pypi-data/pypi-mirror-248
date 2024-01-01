# socks-client

The `socks-client` package provides a core proxy client functionality for Python. Supports SOCKS4 proxy and SOCKS5 proxy and provides sync and async APIs. You probably don't need to use `socks-client` directly.

## Features

* **Supports both TCP and UDP client with the implementation of SOCKS5 and SOCKS4 protocol**
* **Supports username/password authentication and no authentication**
* **Driven by the python standard library, no third-party dependencies**

## Installation

**Install with pip if Python version 3.7.0 or higher is available.**

```shell
$ pip install socks-client
```

pypi：https://pypi.org/project/socks-client/

## Usage

**Async TCP Client**

```python
import socks_client.tcp_async as socks
async def tcp_client_through_socks(proxy_host, proxy_port, target_host, target_port):
    tcp_socks = socks.socksocket(
        proxy_type=socks.SOCKS5,
        proxy_host=proxy_host,
        proxy_port=proxy_port,
        username="my_username",
        password="my_password",
        rdns=False,
    )
    await tcp_socks.settimeout(5)
    sock = await tcp_socks.connect(dest_host=target_host, dest_port=target_port)

    reader, writer = await asyncio.open_connection(
        host=None,
        port=None,
        sock=sock,
    )
    request = (
        b"GET / HTTP/1.1\r\n" b"Host: ip.sb\r\n" b"User-Agent: curl/7.64.0\r\n\r\n"
    )
    writer.write(request)
    response = await asyncio.wait_for(reader.read(1024), timeout=1)
```

**Sync TCP Client**

```python
import socks_client.tcp_sync as socks
def tcp_client_through_socks(proxy_host, proxy_port, target_host, target_port):
    tcp_socks = socks.socksocket()
    tcp_socks.setproxy(
        socks.SOCKS5,
        proxy_host,
        proxy_port,
        rdns=False,
        username="my_username",
        password="my_password",
    )
    tcp_socks.settimeout(5)
    tcp_socks.connect_ex((target_host, target_port))
    request = (
        b"GET / HTTP/1.1\r\n" b"Host: ip.sb\r\n" b"User-Agent: curl/7.64.0\r\n\r\n"
    )
    tcp_socks.send(request)
    response_headers = tcp_socks.recv(4096).decode()
```

**Async UDP Client**

```python
import socks_client.udp_async as socks
async def udp_client_through_socks(
    proxy_host, proxy_port, target_host, target_port, message
):
    await socks.setdefaultproxy(
        socks.SOCKS5,
        proxy_host,
        proxy_port,
        rdns=True,
        username="my_username",
        password="my_password",
    )
    socket.socket = socks.socksocket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    await udp_socket.settimeout(5)
    await udp_socket.sendto(message.encode(), (target_host, target_port))
    response, server_address = await udp_socket.recvfrom(1024)
```

**Sync UDP Client**

```python
import socks_client.udp_sync as socks
def udp_client_through_socks(proxy_host, proxy_port, target_host, target_port, message):
    socks.setdefaultproxy(
        socks.SOCKS5,
        proxy_host,
        proxy_port,
        rdns=False,
        username="my_username",
        password="my_password",
    )
    socket.socket = socks.socksocket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.settimeout(5)
    udp_socket.sendto(message.encode(), (target_host, target_port))
    response, server_address = udp_socket.recvfrom(1024)
    print("Response from server:", response.decode())
```

## Reference

* [Amaindex/socks server](https://github.com/Amaindex/asyncio-socks-server.git)
* [Anorov/PySocks](https://github.com/Anorov/PySocks.git)
* [romis2012/python-socks](https://github.com/romis2012/python-socks.git)
