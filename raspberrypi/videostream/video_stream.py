import cv2
import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer

class VideoStreamTrack(MediaPlayer):
    def __init__(self):
        super().__init__('/dev/video0', format='v4l2', options={
            'video_size': '1280x720',
            'framerate': '30',
            'input_format': 'mjpeg',
        })

async def create_offer(pc, track):
    await pc.addTrack(track)
    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)
    return pc.localDescription

class VideoStreamer:
    def __init__(self):
        self.pc = RTCPeerConnection()
        self.track = VideoStreamTrack()

    async def get_offer(self):
        return await create_offer(self.pc, self.track)

    async def set_answer(self, answer):
        await self.pc.setRemoteDescription(answer)

    async def run(self):
        # Keep the connection alive
        await asyncio.sleep(3600)