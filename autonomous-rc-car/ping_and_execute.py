# Requirements: sshpass
# Mac: brew install hudochenkov/sshpass/sshpass 
# Linux: sudo apt-get install sshpass

import os

class PingAndExecute:
    def __init__(self, pi_host, user, password, script_path, venv_path):
        self.pi_host = pi_host
        self.user = user
        self.password = password
        self.script_path = script_path
        self.venv_path = venv_path

    def ping(self):
        response = os.system(f"ping -c 1 {self.pi_host}")
        return response == 0

    def stop_server(self):
        os.system(f"sshpass -p {self.password} ssh -o StrictHostKeyChecking=no {self.user}@{self.pi_host} 'pkill -f {self.script_path}'")

    def execute(self):
        if self.ping():
            print(f"{self.pi_host} ist erreichbar. Führe Skript aus...")
            os.system(f"sshpass -p {self.password} ssh -o StrictHostKeyChecking=no {self.user}@{self.pi_host} 'source {self.venv_path}/bin/activate && python3 {self.script_path}'")
            print("Skript ausgeführt. Drücken Sie Strg+C, um den Server zu stoppen.")
            try:
                while True:
                    pass
            except KeyboardInterrupt:
                print("Stoppe Server...")
                self.stop_server()
        else:
            print(f"{self.pi_host} ist nicht erreichbar.")

if __name__ == "__main__":
    executor = PingAndExecute(
        pi_host="192.168.171.104",
        user="Betsy",
        password="Betsy123456",
        script_path="autonomous-rc-car-raspberrypi/rc-car-raspberry/run.py",
        venv_path="autonomous-rc-car-raspberrypi/rc-car-raspberry/pi_env"
    )
    executor.execute()
