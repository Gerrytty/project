from concurrent import futures

import grpc
import data_pb2_grpc as pb2_grpc
import data_pb2 as pb2

from threading import Thread
import asyncio
import websockets
import threading


class ChartUpdater(Thread):
    def __init__(self, address, port):
        super().__init__()
        self.data = None
        self.address = address
        self.port = port
        self.conditional_variable = threading.Condition()

    async def update_chart(self, websocket, path):
        while True:
            with self.conditional_variable:
                self.conditional_variable.wait()
            await websocket.send(str(self.data))

    def start(self) -> None:
        start_server = websockets.serve(self.update_chart, self.address, self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()


class BidirectionalService(pb2_grpc.BidirectionalStreamingServicer):

    def __init__(self, received_messages, chart_updater):
        self.received_messages = received_messages
        self.chart_updater = chart_updater

    def GetServerResponse(self, request_iterator, context):
        for message in request_iterator:
            self.received_messages.append(message)
            print(message)

            with self.chart_updater.conditional_variable:
                self.chart_updater.conditional_variable.notifyAll()
                self.chart_updater.data = message.normalizeFitness

            yield pb2.ServerReply(status=202)
        self.received_messages.clear()


class Receiver(Thread):
    def __init__(self, host, port, chart_updater):
        super().__init__()
        self.received_messages = []
        self.chart_updater = chart_updater

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        pb2_grpc.add_BidirectionalStreamingServicer_to_server(BidirectionalService(self.received_messages, chart_updater), self.server)
        self.server.add_insecure_port(f"{host}:{port}")

    def run(self) -> None:
        self.server.start()
        self.server.wait_for_termination()


if __name__ == '__main__':
    chart_updater = ChartUpdater("172.20.10.5", 8081)
    receiver = Receiver("172.20.10.5", 8085, chart_updater)
    receiver.start()
    chart_updater.start()
