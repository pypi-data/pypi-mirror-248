import websockets, asyncio

__all__ = ["Client"]


class Client:
    def __init__(self, url: str, channels: list[str] = []):
        self.url = url
        self.channels = channels

    def onConnect(self):
        pass

    def onRecv(self, msg):
        pass

    def onError(self, e):
        pass

    async def _recv(self, socket):
        try:
            for channel in self.channels:
                await socket.send(channel)
            async for msg in socket:
                self.onRecv(msg)
        except websockets.ConnectionClosed as e:
            self.onError(e)
        except websockets.InvalidStatus as e:
            self.onError(e)
        except RuntimeError as e:
            raise RuntimeError("Two coroutines call recv() concurrently.")
        except TypeError as e:
            raise TypeError("Message doesn’t have a supported type.")

    async def recv(self):
        try:
            async with websockets.connect(self.url) as socket:
                self.onConnect()
                await self._recv(socket)
        except websockets.InvalidURI as e:
            raise e
        except OSError as e:
            raise OSError("TCP connection fails.")
        except websockets.InvalidHandshake as e:
            raise websockets.InvalidHandshake("Opening handshake fails.")
        except asyncio.TimeoutError as e:
            raise asyncio.TimeoutError("Opening handshake times out.")
