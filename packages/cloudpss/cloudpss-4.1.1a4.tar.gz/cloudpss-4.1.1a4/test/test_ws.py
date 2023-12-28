from aiohttp import ClientSession, WSMsgType


# websocket
async def websocket_connect(url, open_func):
    
    # session = await ClientSession()
    # ws = await session.ws_connect(url)

    async with ClientSession() as session:
        async with session.ws_connect(url) as ws:
            open_func()
            async for msg in ws:
                # yield msg
                print(msg)
            return ws