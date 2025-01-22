import socket
import os

class RCClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send_command(self, command):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.host, self.port))
                client_socket.send(command.encode())
                #print(f"Befehl gesendet: {command}")
        except ConnectionError as e:
            print(f"Fehler beim Verbinden: {e}")

    def send_servo_command(self, angle):
        command = f"servo:{angle}"
        self.send_command(command)

    def send_throttle_command(self, throttle):
        command = f"throttle:{throttle}"
        self.send_command(command)

if __name__ == "__main__":
    client = RCClient(host="192.168.171.104", port=4000)  # IP und Port des Raspberry Pi
    
    # Beispielbefehle senden
    client.send_servo_command(90)
    client.send_throttle_command(0.1)