
import cv2

WHITE = [255, 255, 255]

face_cascade = cv2.CascadeClassifier('Haar/haarcascade_frontalcatface.xml')
eye_cascade = cv2.CascadeClassifier('Haar/haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

def draw_box(Image, x, y, w, h):
    cv2.line(Image, (x, y), (int(x + (w/5)) ,y), WHITE, 2)
    cv2.line(Image, (int(x+((w/5)*4)), y), (x+w, y), WHITE, 2)
    cv2.line(Image, (x, y), (x, int(y+(h/5))), WHITE, 2)
    cv2.line(Image, (x+w, y), (x+w, int(y+(h/5))), WHITE, 2)
    cv2.line(Image, (x, int((y+(h/5*4)))), (x, y+h), WHITE, 2)
    cv2.line(Image, (x, (y+h)), (int(x + (w/5)) ,y+h), WHITE, 2)
    cv2.line(Image, (int(x+((w/5)*4)), y+h), (x + w, y + h), WHITE, 2)
    cv2.line(Image, (x+w, (int(y+(h/5*4)))), (x+w, y+h), WHITE, 2)

 
while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        gray_face = cv2.resize((gray[y: y+h, x: x+w]), (80, 80))

        eyes = eye_cascade.detectMultiScale(gray_face)
        for (ex, ey, ew, eh) in eyes:
            draw_box(gray, x, y, w, h)

    cv2.imshow('Face Detection ', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
