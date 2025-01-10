from src.control.client import RCClient
from src.utils.config import PI_HOST, PI_CONTROL_PORT, PI_STREAM_PORT
import time
from src.camera.livestream import receive_stream

if __name__ == "__main__":
    # Steuerbefehle senden
    client = RCClient(host=PI_HOST, port=PI_CONTROL_PORT)

    #Konsolen-Befhl zum akzeptieren des SSH-Keys: ssh pi@192.168.171.104
    #client.send_command("throttle:1")
    #client.send_command("throttle:0.1")
    client.send_throttle_command(1)   
    client.send_throttle_command(0.1)  
    time.sleep(10)
    client.send_throttle_command(0)    
    #client.send_command("servo:90")

    # Livestream empfangen
    motion_url = f"http://{PI_HOST}:{PI_STREAM_PORT}/"
    receive_stream(motion_url)