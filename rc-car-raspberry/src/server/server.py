import socket
import sys
from src.motor_control.motor import MotorControl

class RCServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.motor_control = MotorControl()
        self.server_socket = None

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server läuft auf {self.host}:{self.port}")

        while True:
            conn, addr = self.server_socket.accept()
            print(f"Verbunden mit {addr}")
            data = conn.recv(1024).decode()
            if data:
                print(f"Empfangener Befehl: {data}")
                self.process_command(data)
            conn.close()

    def process_command(self, command):
        print(f"Verarbeite Befehl: {command}")  # Debug-Ausgabe
        if "servo" in command:
            angle = int(command.split(":")[1])
            print(f"Setze Servo auf Winkel: {angle}")  # Debug-Ausgabe
            self.motor_control.set_servo_angle(0, angle)
        elif "throttle" in command:
            throttle = float(command.split(":")[1])
            print(f"Setze Motor auf Geschwindigkeit: {throttle}")  # Debug-Ausgabe
            self.motor_control.set_throttle(1, throttle)

    def shutdown(self, signum, frame):
        print("Server wird heruntergefahren...")
        if self.server_socket:
            self.server_socket.close()
        sys.exit(0)

if __name__ == "__main__":
    server = RCServer(host="0.0.0.0", port=4000)
    server.start()