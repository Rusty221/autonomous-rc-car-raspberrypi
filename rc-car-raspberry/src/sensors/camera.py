# Installiere GStreamer vorher:
# sudo apt install gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good

import os

def start_camera_stream_gstreamer():
    laptop_ip = "192.168.171.119"  # Ersetze mit der IP-Adresse des Laptops
    port = 5000

    gstreamer_command = (
        f"gst-launch-1.0 v4l2src ! "
        f"videoconvert ! "
        f"jpegenc ! "
        f"rtpjpegpay ! "
        f"udpsink host={laptop_ip} port={port}"
    )

    print("Starte GStreamer Kamera-Stream...")
    os.system(gstreamer_command)

def start_camera_stream_ffmpeg():
    laptop_ip = "192.168.171.119"  # Ersetze mit der IP-Adresse des Laptops
    port = 8554

    ffmpeg_command = (
        f"ffmpeg -f v4l2 -i /dev/video0 -vcodec libx264 -f rtsp rtsp://{laptop_ip}:{port}/stream"
    )

    print("Starte FFmpeg Kamera-Stream...")
    os.system(ffmpeg_command)

def start_camera_stream_rtsp():
    laptop_ip = "192.168.171.119"  # Ersetze mit der IP-Adresse des Laptops
    port = 8554

    rtsp_command = (
        f"gst-launch-1.0 v4l2src ! "
        f"videoconvert ! "
        f"x264enc tune=zerolatency ! "
        f"rtph264pay config-interval=1 pt=96 ! "
        f"udpsink host={laptop_ip} port={port}"
    )

    print("Starte RTSP Kamera-Stream...")
    os.system(rtsp_command)

def start_camera_stream_http():
    laptop_ip = "192.168.171.119"  # Ersetze mit der IP-Adresse des Laptops
    port = 8080

    http_command = (
        f"gst-launch-1.0 v4l2src ! "
        f"videoconvert ! "
        f"jpegenc ! "
        f"multipartmux ! "
        f"tcpserversink host={laptop_ip} port={port}"
    )
    
def start_camera_stream_motion():

    cmd = "sudo systemctl start motion"
    print("Starte Motion Kamera-Stream...")
    os.system(cmd)


    print("Starte HTTP/MJPEG Kamera-Stream...")
    os.system(http_command)

if __name__ == "__main__":
    # Wähle die gewünschte Methode zum Starten des Kamera-Streams
    # start_camera_stream_gstreamer()
    # start_camera_stream_ffmpeg()
    # start_camera_stream_rtsp()
    # start_camera_stream_http()
    start_camera_stream_motion()