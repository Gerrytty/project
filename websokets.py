import asyncio
import websockets
import random
from threading import Thread


class ChartUpdater(Thread):
    def __init__(self, address, port):
        super().__init__()
        self.start_server = websockets.serve(self.update_chart, address, port)
        self.data = None

    async def update_chart(self, websocket, path):
        while True:
            if self.data is None:
                await websocket.send(str(random.randint(0, 50)))
            await asyncio.sleep(3)

    def start(self) -> None:
        asyncio.get_event_loop().run_until_complete(self.start_server)
        asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    chart_updater = ChartUpdater("0.0.0.0", 8080)
    chart_updater.start()
