import socket

class RCClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send_command(self, command):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.host, self.port))
                client_socket.send(command.encode())
                print(f"Befehl gesendet: {command}")
        except ConnectionError as e:
            print(f"Fehler beim Verbinden: {e}")

if __name__ == "__main__":
    client = RCClient(host="192.168.171.104", port=4000)  # IP und Port des Raspberry Pi
    client.send_command("servo:90")  # Beispielbefehl
    client.send_command("throttle:0.1")