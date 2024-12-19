import cv2

def receive_stream(ffmpeg_url):
    print(f"Versuche, den Stream von {ffmpeg_url} zu öffnen...")
    cap = cv2.VideoCapture(ffmpeg_url)

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

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    ffmpeg_url = "rtsp://<IP-ADRESSE>:<PORT>/stream"
    receive_stream(ffmpeg_url)
