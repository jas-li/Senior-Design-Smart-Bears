import socket
import time

client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
client.connect(("CC:F9:E4:2C:2B:BB", 4))

try:
  while True:
    time.sleep(1)
    message = "Hi"
    client.send(message.encode('utf-8'))
    data = client.recv(1024)
    if not data:
      break
    print(f"Message: {data.decode('utf-8')}")
except OSError as e:
  pass

client.close()