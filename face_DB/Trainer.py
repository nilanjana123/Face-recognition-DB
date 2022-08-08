
import os
import cv2
import numpy as np
from PIL import Image

EigenFace = cv2.face.EigenFaceRecognizer_create(15)
FisherFace = cv2.face.FisherFaceRecognizer_create(2)
LBPHFace = cv2.face.LBPHFaceRecognizer_create(2, 2, 7, 7)

path = 'dataSet2'
def getImageWithID (path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    FaceList = []
    IDs = []
    for imagePath in imagePaths:
        faceImage = Image.open(imagePath).convert('L')
        faceImage = faceImage.resize((90,90))
        faceNP = np.array(faceImage, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split('.')[1])
        FaceList.append(faceNP)
        IDs.append(ID)
        cv2.imshow('Training', faceNP)
        cv2.waitKey(1)
    return np.array(IDs), FaceList
IDs, FaceList = getImageWithID(path)

print('TRAINING......')
LBPHFace.train(FaceList, IDs)
LBPHFace.save('TrainingData2/trainingData1.xml')
print('1 st model trained!')

EigenFace.train(FaceList, IDs)
EigenFace.save('TrainingData2/trainingData2.xml')
print('2 nd model trained!')

FisherFace.train(FaceList, IDs)
FisherFace.save('TrainingData2/trainingData3.xml')
print('3 rd model trained!')


cv2.destroyAllWindows()
