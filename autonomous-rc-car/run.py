from src.control.client import RCClient
from src.camera.livestream import receive_stream
from src.utils.config import PI_HOST, PI_CONTROL_PORT, PI_STREAM_PORT

if __name__ == "__main__":
    # Steuerbefehle senden
    client = RCClient(host=PI_HOST, port=PI_CONTROL_PORT)
    client.send_command("servo:120")
    client.send_command("throttle:0.1")

    # Livestream empfangen
    gstreamer_url = f"udp://{PI_HOST}:{PI_STREAM_PORT}"
    receive_stream(gstreamer_url)