
from websockets.sync.client import connect

def hello():
    with connect("ws://192.168.50.234:8765") as websocket:
        websocket.send("Hello world!")
        message = websocket.recv()
        print(f"Received: {message}")

hello()