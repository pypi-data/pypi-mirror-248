# Nextcord Health Check

A small Python 3 library and command line app to automate Docker health checks for [nextcord](https://docs.nextcord.dev/en/stable/index.html) bots.

## Installation

`pip install nextcordhealthcheck`

This will install both the Python library and the command line app, the python library is importable using `import nextcordhealthcheck` and the CLI app by using the command `nextcordhealthcheck`.

## How It Works & Usage Examples

### Python Library (Server)

The library has 1 function, `start`.

`start` takes a `nextcord.Client` object as well as optional parameters, and returns an awaitable that produces a `asyncio.base_events.Server`:

```python
def start(
    client: nextcord.client,
    port: int = 40404,
    bot_max_latency: float = 0.5
) -> Awaitable[asyncio.base_events.Server]
```

`start` calls [`asyncio.start_server`](https://docs.python.org/3/library/asyncio-stream.html#asyncio.start_server), creating an asyncio TCP socket server which listens for connections. Once a client connects, it tests the nextcord client for various things that indicate its health (latency, login status, etc.), and the result of this health check is then sent to the healthcheck client.

The returned `Server` object can be used to stop the server (e.g. `healthcheck_server.close()`)

The default port for the socket server is `40404`, if you change it you will need to use the `--port` flag on the client as well.

```python
import nextcord
import nextcordhealthcheck

class CustomClient(nextcord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.healthcheck_server = None

    async def on_ready(self):
        if self.healthcheck_server is None:
            self.healthcheck_server = await nextcordhealthcheck.start(self)
            # Later you can close or check on self.healthcheck_server
```

### CLI App (Client)

The CLI app is a simple client that connects to the server and determines its exit code from what the server sends; `0`
for healthy, `1` for unhealthy.

Here's an example of using in a Dockerfile:

```dockerfile
FROM python:3.11-slim-buster

# Copy files, install requirements, setup bot, etc.

RUN pip install nextcordhealthcheck

# The `|| exit 1` isn't required but it's good practice anyway.
HEALTHCHECK CMD nextcordhealthcheck || exit 1

CMD ["python", "/path/to/bot.py"]
```
