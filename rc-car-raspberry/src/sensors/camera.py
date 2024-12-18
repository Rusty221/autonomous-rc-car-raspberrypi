# Installiere GStreamer vorher:
# sudo apt install gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good

import os

def start_camera_stream():
    # IP-Adresse des Laptops und Port
    laptop_ip = "192.168.171.119"  # Ersetze mit der IP-Adresse des Laptops
    port = 5000

    # GStreamer-Befehl für Livestream
    gstreamer_command = (
        f"gst-launch-1.0 v4l2src ! "
        f"videoconvert ! "
        f"jpegenc ! "
        f"rtpjpegpay ! "
        f"udpsink host={laptop_ip} port={port}"
    )

    print("Starte Kamera-Stream...")
    os.system(gstreamer_command)

if __name__ == "__main__":
    start_camera_stream()