import json
import paho.mqtt.client as mqtt
from aiortc import RTCSessionDescription

class MQTTSignaling:
    def __init__(self, broker, port, username, password):
        self.client = mqtt.Client()
        self.client.username_pw_set(username, password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(broker, port, 60)
        self.offer_callback = None
        self.answer_callback = None

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        client.subscribe("webrtc/signaling")

    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload)
        if data['type'] == 'offer' and self.offer_callback:
            self.offer_callback(RTCSessionDescription(**data))
        elif data['type'] == 'answer' and self.answer_callback:
            self.answer_callback(RTCSessionDescription(**data))

    def send_offer(self, offer):
        self.client.publish("webrtc/signaling", json.dumps({
            "type": offer.type,
            "sdp": offer.sdp
        }))

    def send_answer(self, answer):
        self.client.publish("webrtc/signaling", json.dumps({
            "type": answer.type,
            "sdp": answer.sdp
        }))

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()