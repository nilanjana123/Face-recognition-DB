
import cv2                  # Importing the opencv
import NameFind

face_cascade = cv2.CascadeClassifier('Haar/haarcascade_frontalcatface.xml')
#eye_cascade = cv2.CascadeClassifier('Haar/haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        gray_face = cv2.resize((gray[y: y+h, x: x+w]), (80, 80))
        """
        eyes = eye_cascade.detectMultiScale(gray_face)
        for (ex, ey, ew, eh) in eyes:
            NameFind.draw_box(gray, x, y, w, h)
        """
        NameFind.draw_box(gray, x, y, w, h)
    cv2.imshow('Face Detection ', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
