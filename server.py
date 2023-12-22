import asyncio
import logging
import websockets
import names
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK

logging.basicConfig(level=logging.INFO)


class Server:
    clients = set()

    async def register(self, wss: WebSocketServerProtocol):
        wss.name = names.get_full_name()
        self.clients.add(wss)
        logging.info(f"{wss.remote_address} connects")

    async def unregister(self, wss: WebSocketServerProtocol):
        self.clients.remove(wss)
        logging.info(f"{wss.remote_address} disconnects")

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, wss: WebSocketServerProtocol):
        await self.register(wss)
        try:
            await self.distrubute(wss)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(wss)

    async def distrubute(self, wss: WebSocketServerProtocol):
        async for message in wss:
            await self.send_to_clients(f"{wss.name}: {message}")


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, "localhost", 8080):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
