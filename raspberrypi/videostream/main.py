import asyncio
from video_stream import VideoStreamer
from mqtt_signaling import MQTTSignaling

async def main():
    # Initialize VideoStreamer
    streamer = VideoStreamer()

    # Initialize MQTT Signaling
    signaling = MQTTSignaling(
        broker="your.mqtt.broker",
        port=1883,
        username="your_username",
        password="your_password"
    )

    # Set up callbacks
    async def on_offer(offer):
        answer = await streamer.get_offer()
        signaling.send_answer(answer)

    async def on_answer(answer):
        await streamer.set_answer(answer)

    signaling.offer_callback = on_offer
    signaling.answer_callback = on_answer

    # Start MQTT client
    signaling.start()

    # Get and send initial offer
    offer = await streamer.get_offer()
    signaling.send_offer(offer)

    # Run the video streamer
    await streamer.run()

if __name__ == "__main__":
    asyncio.run(main())