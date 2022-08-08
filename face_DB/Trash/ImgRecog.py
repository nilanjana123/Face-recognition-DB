import cv2
import numpy as np
import NameFind
import os
from PIL import Image



face_cascade = cv2.CascadeClassifier('Haar/haarcascade_frontalcatface.xml')


LBPH = cv2.face.LBPHFaceRecognizer_create(2, 2, 7, 7, 20)


LBPH.read("TrainingData/trainingData1.xml")

inputIMG = input('Enter Image name with path\n')



img = cv2.imread(inputIMG)


def predict(image):



    i,c = LBPH.predict(image)

    path = 'dataSet'
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    for imagePath in imagePaths:
        faceImage = Image.open(imagePath).convert('L')  # Room for improvement
        faceImage = faceImage.resize((110, 110))
        faceNP = np.array(faceImage, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split('.')[1])
        if ID is i:

            NAME = NameFind.ID2Name(ID, c)
            print(NAME)
            NameFind.DispID(x, y, w, h, NAME, image)
            break









gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 4)
print(faces)

for (x, y, w, h) in faces:

    Face = cv2.resize((gray[y: y + h, x: x + w]), (110, 110))

    predict(Face)
    """
    ID, conf = LBPH.predict(Face)
    print(ID)
    NAME = NameFind.ID2Name(ID, conf)
    NameFind.DispID(x, y, w, h, NAME, gray)
    """
cv2.imshow('LBPH Image Recognition System', gray)
cv2.waitKey(0)
cv2.destroyAllWindows()
