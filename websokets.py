import asyncio
import time

import websockets
from threading import Thread
import threading


def receive_data(chart_updater):
    i = 0
    while True:
        i += 1
        time.sleep(3)
        with chart_updater.conditional_variable:
            chart_updater.conditional_variable.notifyAll()
            chart_updater.data = i


class ChartUpdater(Thread):
    def __init__(self, address, port):
        super().__init__()
        self.start_server = websockets.serve(self.update_chart, address, port)
        self.data = None
        self.conditional_variable = threading.Condition()

    async def update_chart(self, websocket, path):
        while True:
            with self.conditional_variable:
                self.conditional_variable.wait()
            await websocket.send(str(self.data))

    def start(self) -> None:
        asyncio.get_event_loop().run_until_complete(self.start_server)
        asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    chart_updater = ChartUpdater("0.0.0.0", 8080)

    thread_to_receive_data = Thread(target=receive_data, args=(chart_updater, ))
    thread_to_receive_data.start()

    chart_updater.start()
