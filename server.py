import asyncio
import os
import websockets

connected_clients = set()


async def handle_client(websocket):

    connected_clients.add(websocket)

    print("Client connected!")

    try:

        async for message in websocket:

            print("Received:", message)

            for client in connected_clients:

                if client != websocket:
                    await client.send(message)

    except websockets.exceptions.ConnectionClosed:

        print("Client disconnected!")

    finally:

        connected_clients.remove(websocket)


async def main():

    port = int(os.environ.get("PORT", 8765))

    async with websockets.serve(
        handle_client,
        "0.0.0.0",
        port
    ):

        print("WebSocket server running on port", port)

        await asyncio.Future()


asyncio.run(main())