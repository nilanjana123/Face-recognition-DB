

import cv2
import numpy as np
import sqlite3
import math

WHITE = [255, 255, 255]

face_cascade = cv2.CascadeClassifier('Haar/haarcascade_frontalcatface.xml')
eye_cascade = cv2.CascadeClassifier('Haar/haanilurcascade_eye.xml')
glass_cas = cv2.CascadeClassifier('Haar/haarcascade_eye_tree_eyeglasses.xml')

print('Caution : IF YOU TRY TO UPDATE UNKNOWN ID NEW USER WILL BE ADDED WITH THE FOLLOWING ID\n')
ID = input('Enter ID')
name = input('Enter Name')


def DetectEyes(Image):
    Theta = 0
    rows, cols = Image.shape
    glass = glass_cas.detectMultiScale(Image)
    for (sx, sy, sw, sh) in glass:
        if glass.shape[0] == 2:
            if glass[1][0] > glass[0][0]:
                DY = ((glass[1][1] + glass[1][3] / 2) - (
                            glass[0][1] + glass[0][3] / 2))
                DX = ((glass[1][0] + glass[1][2] / 2) - glass[0][0] + (
                            glass[0][2] / 2))
            else:
                DY = (-(glass[1][1] + glass[1][3] / 2) + (
                            glass[0][1] + glass[0][3] / 2))
                DX = (-(glass[1][0] + glass[1][2] / 2) + glass[0][0] + (
                            glass[0][2] / 2))

            if (DX != 0.0) and (DY != 0.0):
                Theta = math.degrees(math.atan(round(float(DY) / float(DX), 2)))

                M = cv2.getRotationMatrix2D((cols / 2, rows / 2), Theta, 1)
                Image = cv2.warpAffine(Image, M, (cols, rows))
                cv2.imshow('ROTATED', Image)

                Face2 = face_cascade.detectMultiScale(Image, 1.3, 5)
                for (FaceX, FaceY, FaceWidth, FaceHeight) in Face2:
                    CroppedFace = Image[FaceY: FaceY + FaceHeight, FaceX: FaceX + FaceWidth]
                    return CroppedFace


def insertorUpdate(id,name):
    conn = sqlite3.connect("people.db")
    cmd = "insert into fdb2(id,name) values (" + str(id) + "," + str(name) + ");"
    conn.execute(cmd)
    conn.commit()
    conn.close()
Count = 0
insertorUpdate(ID,name)
cap = cv2.VideoCapture(0)

while Count < 100:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if np.average(gray) > 90:
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            FaceImage = gray[y - int(h / 2): y + int(h * 1.5), x - int(x / 2): x + int(w * 1.5)]
            Img = (DetectEyes(FaceImage))
            cv2.putText(gray, "FACE DETECTED", (int(x + (w / 2)), y - 5), cv2.FONT_HERSHEY_DUPLEX, .4, WHITE)
            if Img is not None:
                frame = Img
            else:
                frame = gray[y: y + h, x: x + w]
            cv2.imwrite("dataSet2/User." + str(ID) + "." + str(Count) + ".jpg", frame)
            cv2.waitKey(300)
            cv2.imshow("CAPTURED PHOTO", frame)
            Count = Count + 1
            print(100 - int(Count))
    cv2.imshow('Face Capture', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
