from src.control.client import RCClient
from src.camera.livestream import receive_stream as receive_gstreamer_stream
from src.camera.livestream_ffmpeg import receive_stream as receive_ffmpeg_stream
from src.camera.livestream_rtsp import receive_stream as receive_rtsp_stream
from src.camera.livestream_http import receive_stream as receive_http_stream
from src.utils.config import PI_HOST, PI_CONTROL_PORT, PI_STREAM_PORT

if __name__ == "__main__":
    # Steuerbefehle senden
    client = RCClient(host=PI_HOST, port=PI_CONTROL_PORT)
    client.send_command("servo:90")
    client.send_command("throttle:0.1")

    # Livestream empfangen
    gstreamer_url = f"udp://{PI_HOST}:{PI_STREAM_PORT}"
    # receive_gstreamer_stream(gstreamer_url)

    ffmpeg_url = f"rtsp://{PI_HOST}:{PI_STREAM_PORT}/stream"
    receive_ffmpeg_stream(ffmpeg_url)

    rtsp_url = f"rtsp://{PI_HOST}:{PI_STREAM_PORT}/stream"
    # receive_rtsp_stream(rtsp_url)

    http_url = f"http://{PI_HOST}:{PI_STREAM_PORT}/stream.mjpg"
    # receive_http_stream(http_url)