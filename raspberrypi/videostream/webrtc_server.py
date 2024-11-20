# import asyncio
# import json
# from aiohttp import web
# from aiortc import RTCPeerConnection, RTCSessionDescription
# from aiortc.contrib.media import MediaPlayer

# async def offer(request):
#     params = await request.json()
#     offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
    
#     pc = RTCPeerConnection()
    
#     @pc.on("connectionstatechange")
#     async def on_connectionstatechange():
#         print("Connection state is:", pc.connectionState)
    
#     # player = MediaPlayer("udp://192.168.1.1:5000")
#     player = MediaPlayer("udp://127.0.0.1:5000")
#     pc.addTrack(player.video)
    
#     await pc.setRemoteDescription(offer)
#     answer = await pc.createAnswer()
#     await pc.setLocalDescription(answer)
    
#     return web.Response(
#         content_type="application/json",
#         text=json.dumps({
#             "sdp": pc.localDescription.sdp,
#             "type": pc.localDescription.type
#         })
#     )

# async def on_shutdown(app):
#     # close peer connections
#     coros = [pc.close() for pc in pcs]
#     await asyncio.gather(*coros)
#     pcs.clear()

# app = web.Application()
# app.router.add_post("/offer", offer)
# app.on_shutdown.append(on_shutdown)
# web.run_app(app, host="0.0.0.0", port=8080)


import asyncio
import json
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer
import aiohttp_cors

async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
    pc = RTCPeerConnection()

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print("Connection state is:", pc.connectionState)

    player = MediaPlayer("udp://127.0.0.1:5000")
    pc.addTrack(player.video)

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.Response(
        content_type="application/json",
        text=json.dumps({
            "sdp": pc.localDescription.sdp,
            "type": pc.localDescription.type
        })
    )

async def on_shutdown(app):
    # close peer connections
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()

app = web.Application()
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )
})

cors.add(app.router.add_post("/offer", offer))

app.on_shutdown.append(on_shutdown)
web.run_app(app, host="0.0.0.0", port=8080)