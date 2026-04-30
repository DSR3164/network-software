import asyncio
import websockets
import json

# Простой Signaling сервер для WebRTC
# Он должен пересылать сообщения от одного клиента всем остальным (или конкретному собеседнику)

CONNECTIONS = set()

async def handler(ws):
    CONNECTIONS.add(ws)
    try:
        async for msg in ws:
            data = json.loads(msg)

            for c in CONNECTIONS:
                if c != ws:
                    await c.send(json.dumps(data))

    finally:
        CONNECTIONS.remove(ws)

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
