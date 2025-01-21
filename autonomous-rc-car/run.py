import threading
import time
import cv2
import numpy as np

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

def find_two_largest_contours(mask):
    """ Hilfsfunktion, um die zwei größten Konturen zurückzugeben. """
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) < 2:
        # Falls weniger als zwei Konturen vorhanden sind, einfach alle zurückgeben
        contours_sorted = sorted(contours, key=cv2.contourArea, reverse=True)
        return contours_sorted
    else:
        # Sortiere nach Fläche (absteigend) und nimm die zwei größten
        contours_sorted = sorted(contours, key=cv2.contourArea, reverse=True)
        return contours_sorted[:2]

def detect_orange_lines(frame):
    """
    Versucht zwei orange Linien zu erkennen.
    Gibt die X-Koordinaten der Mittelpunkte dieser Linien zurück.
    """
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Orange Farbfilter
    lower_orange = (5, 100, 80)
    upper_orange = (25, 255, 255)

    # Maske erzeugen
    mask = cv2.inRange(hsv, lower_orange, upper_orange)

    # Erosion, Dilation zur Rauschunterdrückung
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)

    # Zwei größte Konturen suchen
    contours = find_two_largest_contours(mask)
    cx_list = []

    for c in contours:
        area = cv2.contourArea(c)
        if area > 50:  # Schwellwert für minimale Konturgröße
            M = cv2.moments(c)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cx_list.append(cx)
                # Zur Visualisierung: Mittelpunkt zeichnen
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

    return cx_list, mask


def main():
    # 1) Starte Neben-Thread für die Steuer-Logik
    #control_thread = threading.Thread(target=steering_logic)
    #control_thread.start()
    client = RCClient(host=config.PI_HOST, port=config.PI_CONTROL_PORT)

    # 2) Hier im Haupt-Thread den Stream anzeigen
    motion_url = f"http://{config.PI_HOST}:{config.PI_STREAM_PORT}/"
    cap = cv2.VideoCapture(motion_url)

    if not cap.isOpened():
        print("Fehler: Livestream konnte nicht geöffnet werden.")
        return
    
    print("Livestream wird angezeigt. Drücke 'q', um zu beenden.")

    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Fehler beim Lesen des Streams.")
                break
            
            frame_blur = cv2.GaussianBlur(frame, (5, 5), 0)
            
            # Orange Konturen suchen
            cx_list, mask = detect_orange_lines(frame_blur)
            

            # Wenn wir mindestens zwei Linien haben
            if len(cx_list) >= 2:
                
                # Sortiere die Mittelpunkte
                cx_list.sort()
                left_x = cx_list[0]
                right_x = cx_list[1]

                # Mitte zwischen den beiden Linien
                mid_x = (left_x + right_x) // 2

                # Bildmitte
                width = frame.shape[1]
                center = width // 2

                offset = mid_x - center  # negativ: Linie(n) liegt/liegen links, positiv: rechts

                # Lenkwinkel ableiten:
                base_servo = 90
                gain = 0.05  # An wie vielen "Pixel pro Grad" du anpasst
                new_servo = int(base_servo + gain * offset)
                new_servo = max(60, min(120, new_servo))  # Begrenze auf [60..120]

                # Kommandos ans Auto
                client.send_command(f"servo:{new_servo}")
                
                # Gas geben
                client.send_throttle_command(0.15)

            else:
                # Wir haben keine oder nur 1 Kontur gefunden
                client.send_throttle_command(0.0)
                print("Weniger als 2 Linien erkannt, Anhalten!")

            # Anzeigen
            #cv2.imshow("RC Car Livestream", frame)
            cv2.imshow("blurred frame", frame_blur)
            cv2.imshow("Orange Mask Blur", mask)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Programm wird beendet.")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        # Motor aus!
        client.send_throttle_command(0)
        print("Programm beendet.")

    # 3) Warten, bis der Steuer-Thread fertig ist (optional)
    #control_thread.join()

if __name__ == "__main__":
    main()