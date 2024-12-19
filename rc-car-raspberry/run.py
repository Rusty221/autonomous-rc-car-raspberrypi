import threading
import signal
import sys
from src.server.server import RCServer
from src.sensors.camera import start_camera_stream

def shutdown_server(signum, frame):
    print("Server wird heruntergefahren...")
    server.shutdown(signum, frame)
    sys.exit(0)

if __name__ == "__main__":
    # Server für Steuerbefehle starten
    server = RCServer(host="0.0.0.0", port=4000)
    server_thread = threading.Thread(target=server.start)
    server_thread.start()

    # Signalbehandlung in den Hauptthread verschieben
    signal.signal(signal.SIGINT, shutdown_server)

    # Kamera-Stream starten
    start_camera_stream()