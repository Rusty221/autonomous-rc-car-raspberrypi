import os

def start_camera_stream_motion():
    cmd = "sudo systemctl start motion"
    print("Starte Motion Kamera-Stream...")
    os.system(cmd)

if __name__ == "__main__":
    start_camera_stream_motion()