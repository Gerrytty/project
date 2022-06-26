from __future__ import print_function

import grpc
import grpc_client.data_pb2_grpc as pb2_grpc
import grpc_client.data_pb2 as pb2
import time

from threading import Thread

current_population = 0


def increment_population(sender):
    while True:
        sender.current_population += 1
        sender.message = (0, 1, 1, [1], [1])
        time.sleep(5)


def make_message(generation, fitness, normalize_fitness, weights, delays):
    return pb2.Message(generation=generation,
                       fitness=fitness,
                       normalizeFitness=normalize_fitness,
                       weights=weights,
                       delays=delays)


# 172.20.10.5
class Sender(Thread):
    def __init__(self, ip_address, port):
        super().__init__()
        self.current_population = 0
        self.ip_address = ip_address
        self.port = port
        self.message = None
        self.current_population = -1
        self.current_response = None

    def send_message(self, stub):
        responses = stub.GetServerResponse(self.generate_messages())
        for response in responses:
            self.current_response = response
            print(f"New response = {response}")

    def generate_messages(self):
        curr_pop = -1
        while True:
            if self.current_population != curr_pop and self.message is not None:
                curr_pop += 1
                yield self.message
            time.sleep(1)

    def run(self) -> None:
        with grpc.insecure_channel(f"{self.ip_address}:{self.port}") as channel:
            stub = pb2_grpc.BidirectionalStreamingStub(channel)
            self.send_message(stub)


if __name__ == '__main__':
    # sender to server
    s = Sender("172.20.10.5", 8080)
    s.start()

    # main ga
    increment_population(s)
