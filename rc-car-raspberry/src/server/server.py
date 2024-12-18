import socket
from src.motor_control.motor import MotorControl

class RCServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.motor_control = MotorControl()

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server läuft auf {self.host}:{self.port}")

        while True:
            conn, addr = server_socket.accept()
            print(f"Verbunden mit {addr}")
            data = conn.recv(1024).decode()
            if data:
                print(f"Empfangener Befehl: {data}")
                self.process_command(data)
            conn.close()

    def process_command(self, command):
        if "servo" in command:
            angle = int(command.split(":")[1])
            self.motor_control.set_servo_angle(0, angle)
        elif "throttle" in command:
            throttle = float(command.split(":")[1])
            self.motor_control.set_throttle(1, throttle)

if __name__ == "__main__":
    server = RCServer(host="0.0.0.0", port=4000)
    server.start()