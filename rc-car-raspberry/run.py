import threading
from src.server.server import RCServer
from src.sensors.camera import start_camera_stream

if __name__ == "__main__":
    # Server für Steuerbefehle starten
    server = RCServer(host="0.0.0.0", port=4000)
    server_thread = threading.Thread(target=server.start)
    server_thread.start()

    # Kamera-Stream starten
    start_camera_stream()