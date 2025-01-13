import threading
import time
import cv2

from src.control.client import RCClient
import src.utils.config as config

def steering_logic():
    """
    Hier kannst du deine Befehle an den RCClient schicken,
    während im Hauptthread das Video gezeigt wird.
    """
    client = RCClient(host=config.PI_HOST, port=config.PI_CONTROL_PORT)
    time.sleep(1)
    client.send_command("servo:120")
    time.sleep(1)
    client.send_command("servo:60")
    time.sleep(1)
    client.send_command("servo:90")
    time.sleep(1)
    client.send_throttle_command(0.15)
    time.sleep(2)
    client.send_throttle_command(0)
    print("Steuer-Thread beendet.")


def main():
    # 1) Starte Neben-Thread für die Steuer-Logik
    control_thread = threading.Thread(target=steering_logic)
    control_thread.start()

    # 2) Hier im Haupt-Thread den Stream anzeigen
    motion_url = f"http://{config.PI_HOST}:{config.PI_STREAM_PORT}/"
    cap = cv2.VideoCapture(motion_url)

    if not cap.isOpened():
        print("Fehler: Livestream konnte nicht geöffnet werden.")
        return
    
    print("Livestream wird angezeigt. Drücke 'q', um zu beenden.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Fehler beim Lesen des Streams.")
            break

        cv2.imshow("RC Car Livestream", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # 3) Warten, bis der Steuer-Thread fertig ist (optional)
    control_thread.join()
    print("Fertig!")

if __name__ == "__main__":
    main()