import cv2

def receive_stream(gstreamer_url):
    cap = cv2.VideoCapture(gstreamer_url)

    if not cap.isOpened():
        print("Fehler: Livestream konnte nicht geöffnet werden.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Fehler beim Lesen des Streams.")
            break

        cv2.imshow("RC Car Livestream", frame)

        # Beenden mit der Taste 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # GStreamer URL für den Stream (ersetze <IP-ADRESSE> durch die IP des Raspberry Pi)
    gstreamer_url = "udp://192.168.171.104:5000"
    receive_stream(gstreamer_url)