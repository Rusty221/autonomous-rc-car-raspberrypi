import cv2

def receive_stream(gstreamer_url):
    print(f"Versuche, den Stream von {gstreamer_url} zu öffnen...")
    # Öffne den GStreamer-Stream
    cap = cv2.VideoCapture(gstreamer_url, cv2.CAP_GSTREAMER)

    if not cap.isOpened():
        print("Fehler: Livestream konnte nicht geöffnet werden.")
        return
    else:
        print("Livestream wird angezeigt. Drücke 'q', um zu beenden.")
        
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
    gstreamer_url = (
        "udpsrc port=5000 ! "
        "application/x-rtp, encoding-name=JPEG ! "
        "rtpjpegdepay ! "
        "jpegdec ! "
        "videoconvert ! "
        "appsink"
    )
    receive_stream(gstreamer_url)