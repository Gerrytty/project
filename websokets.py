import asyncio
import websockets


async def time(websocket, path):
    while True:
        await websocket.send("hello")
        await asyncio.sleep(1)

start_server = websockets.serve(time, '0.0.0.0', 8080)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()