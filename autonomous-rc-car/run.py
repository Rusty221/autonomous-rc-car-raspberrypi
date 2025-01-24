import threading
import time
import cv2
import numpy as np

from src.control.client import RCClient
import src.utils.config as config

######################################
# TUNING-PARAMETER
######################################

# -- HSV-GRENZEN FÜR ORANGE (OpenCV-Skala 0..180,0..255,0..255) --
HSV_LOWER_ORANGE = (0, 0, 225)
HSV_UPPER_ORANGE = (50, 62, 255)

HSV_LOWER_ORANGE_HUE = (130, 0, 225)
HSV_LOWER_ORANGE_HUE = (180, 62, 255)

# -- KONTUREN --
CONTOUR_THRESHOLD = 2500  # Mindestfläche in Pixel²
MORPH_KERNEL_SIZE = 5      # Kernel-Größe für Dilation/Erosion
MORPH_DILATE_ITER = 4      # Anzahl Iterationen für Dilation

# -- LENKUNG: ZWEI LINIEN --
BASE_SERVO = 90
GAIN_TWO_LINES = 0.11     # offset * GAIN => +/- servo
MIN_SERVO = 60
MAX_SERVO = 120

# -- LENKUNG: EINE LINIE --
GAIN_ONE_LINE = 0.10
ASPIRED_OFFSET_SINGLE_LINE = 250  # z.B. 250px Abstand vom Bildzentrum

# -- GESCHWINDIGKEIT / THROTTLE --
THROTTLE_TWO_LINES = 0.14
THROTTLE_ONE_LINE = 0.15
THROTTLE_NO_LINES = 0.14

######################################
# ENDE TUNING-PARAMETER
######################################



def compute_distance_map(frame, lower_hsv, upper_hsv):
    """
    Erzeugt eine Graustufen-Map, bei der der Wert angibt,
    wie 'weit' jeder Pixel vom HSV-Bereich [lower_hsv, upper_hsv] entfernt ist.

    - frame: BGR-Bild (z. B. vom Kamerastream)
    - lower_hsv, upper_hsv: Tupel (H, S, V) in OpenCV-Skala
    """
    # 1) BGR -> HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    H, S, V = cv2.split(hsv)

    Lh, Ls, Lv = lower_hsv
    Uh, Us, Uv = upper_hsv

    # 2) Hilfsfunktion: Abstand eines Kanals vom [L, U]-Intervall
    def channel_dist(channel, L, U):
        below = (channel < L)
        above = (channel > U)
        # Im Bereich [L, U] => Distanz = 0
        # Darunter => (L - channel), darüber => (channel - U)
        d = np.zeros_like(channel, dtype=np.float32)
        d[below] = (L - channel[below])
        d[above] = (channel[above] - U)
        return d

    dH = channel_dist(H, Lh, Uh)  # Distanz in Hue
    dS = channel_dist(S, Ls, Us)  # Distanz in S
    dV = channel_dist(V, Lv, Uv)  # Distanz in V

    # 3) Gesamtdistanz
    total_dist = dH + dS + dV

    # 4) Normierung auf 0..255
    #    Grobe Schätzung des "max. möglichen" Abstands
    maxDist = (Uh - Lh) + (Us - Ls) + (Uv - Lv)
    if maxDist < 1:
        maxDist = 1  # Vermeidung Division durch 0
    scale_factor = 255.0 / float(maxDist)
    
    dist_map_8u = np.clip(total_dist * scale_factor, 0, 255).astype(np.uint8)

    return dist_map_8u

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

def detect_lines(frame):
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Maske erzeugen
    mask = cv2.inRange(hsv, HSV_LOWER_ORANGE, HSV_UPPER_ORANGE)
    mask_second = cv2.inRange(hsv, HSV_LOWER_ORANGE_HUE, HSV_LOWER_ORANGE_HUE)
    
    mask = cv2.bitwise_or(mask, mask_second)

    # Erosion, Dilation zur Rauschunterdrückung
    kernel = np.ones((5, 5), np.uint8)
    #mask = cv2.erode(mask_combined, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=4)

    # Zwei größte Konturen suchen
    contours = find_two_largest_contours(mask)
    cx_list = []
    

    for c in contours:
        area = cv2.contourArea(c)
        if area > CONTOUR_THRESHOLD:  
            M = cv2.moments(c)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cx_list.append(cx)
                # Zur Visualisierung: Mittelpunkt zeichnen
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

    return cx_list, mask


def main():
    client = RCClient(host=config.PI_HOST, port=config.PI_CONTROL_PORT)

    # 2) Haupt-Thread: Livestream anzeigen
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
            
            #
            dist_map = compute_distance_map(frame_blur, HSV_LOWER_ORANGE, HSV_UPPER_ORANGE)
            
            # Orange Konturen suchen
            cx_list, mask = detect_lines(frame_blur)
            """
            time.sleep(1)
            client.send_command("servo:120")
            time.sleep(1)
            client.send_command("servo:60")
            """
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
                gain = 0.1  
                new_servo = int(base_servo - gain * offset)
                new_servo = max(60, min(120, new_servo))  

                # Kommandos ans Auto
                client.send_command(f"servo:{new_servo}")
                print(f"Servo: {new_servo}")
                
                # Gas geben
                client.send_throttle_command(0.12)
            

            elif len(cx_list) == 1:
                # Nur eine Linie gefunden
                single_x = cx_list[0]

                width = frame.shape[1]
                center = width // 2

                if single_x < center:
                    # linie links
                    desired_x = center - ASPIRED_OFFSET_SINGLE_LINE
                else:
                    # linie rechts 
                    desired_x = center + ASPIRED_OFFSET_SINGLE_LINE

                offset = single_x - desired_x

                new_servo = int(BASE_SERVO - GAIN_ONE_LINE * offset)
                new_servo = max(60, min(120, new_servo))

                client.send_command(f"servo:{new_servo}")
                print(f"Servo: {new_servo}")

                client.send_throttle_command(THROTTLE_ONE_LINE)
                #print("Nur eine Linie gefunden. Lenke nach.")

            else:
                client.send_throttle_command(THROTTLE_NO_LINES)
                print("Keine Linien erkannt. Anhalten!")


            #dist_map = compute_distance_map(frame_blur, HSV_LOWER_ORANGE, HSV_UPPER_ORANGE)
            #colored_dist = cv2.applyColorMap(dist_map, cv2.COLORMAP_JET)
            
            #cv2.imshow("Distance (grayscale)", dist_map)
            #cv2.imshow("Distance Heatmap", colored_dist)
            
            #cv2.imshow("RC Car Livestream", frame)
            cv2.imshow("blurred frame", frame_blur)
            cv2.imshow("Mask with Blur", mask)
            
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

if __name__ == "__main__":
    main()