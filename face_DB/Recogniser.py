
import cv2
import sqlite3
import log

WHITE = [255, 255, 255]

face_cascade = cv2.CascadeClassifier('Haar/haarcascade_frontalcatface.xml')
eye_cascade = cv2.CascadeClassifier('Haar/haarcascade_eye.xml')

recognise_1 = cv2.face.LBPHFaceRecognizer_create(2, 2, 7, 7, 15)
recognise_2 = cv2.face.EigenFaceRecognizer_create(10, 5000)
recognise_3 = cv2.face.FisherFaceRecognizer_create(5, 500)
recognise_1.read("TrainingData2/trainingData1.xml")
recognise_2.read("TrainingData2/trainingData2.xml")
recognise_3.read("TrainingData2/trainingData3.xml")


cap = cv2.VideoCapture(0)


def draw_box(Image, name, x, y, w, h):
    cv2.line(Image, (x, y), (int(x + (w/5)) ,y), WHITE, 2)
    cv2.line(Image, (int(x+((w/5)*4)), y), (x+w, y), WHITE, 2)
    cv2.line(Image, (x, y), (x, int(y+(h/5))), WHITE, 2)
    cv2.line(Image, (x+w, y), (x+w, int(y+(h/5))), WHITE, 2)
    cv2.line(Image, (x, int((y+(h/5*4)))), (x, y+h), WHITE, 2)
    cv2.line(Image, (x, (y+h)), (int(x + (w/5)) ,y+h), WHITE, 2)
    cv2.line(Image, (int(x+((w/5)*4)), y+h), (x + w, y + h), WHITE, 2)
    cv2.line(Image, (x+w, (int(y+(h/5*4)))), (x+w, y+h), WHITE, 2)
    cv2.putText(Image, name, (int(x+ 50), int(y-20)), cv2.FONT_HERSHEY_DUPLEX, .4, WHITE)



def predict(img):
    if img is not None:
        image = img
    else:
        image = gray[y: y + h, x: x + w]

    i1, c1 = recognise_1.predict(image)
    i2, c2 = recognise_2.predict(image)
    i3, c3 = recognise_3.predict(image)

    if (i1==i2 and i1==i3):
        i, c = i1, c1
    elif(i1==i2 or i1==i3):
        i,c=i1,c1
    elif (i2==i3):
        i,c=i2,c2
    else:
        i, c = i1, c1

    ID = i
    profile = log.getFace(ID)
    conn2 = sqlite3.connect("people.db")
    cmd2 = "insert into accuracy(id) values (" + str(profile[0]) + ")"
    conn2.execute(cmd2)
    conn2.commit()

    #print("ID is : " + str(profile[0]) + " and Name is " + profile[1]) #prints the id and name symuntaneously
    #DispID(x, y, w, h, profile[1], image)
    cmd3 = 'select id from (select id,count(id) as "cntid" from accuracy group by id order by "cntid" desc)'
    cursor3 = conn2.execute(cmd3)
    #wonderStr = str(cursor3.fetchone()).split(',')[0].split('(')[1]  #Only one accuracy
    wonderStr2 = str(cursor3.fetchall())
    draw_box(gray, profile[1], x, y, w, h)

    return wonderStr2


while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        gray_face = cv2.resize((gray[y: y + h, x: x + w]), (90, 90))
        eyes = eye_cascade.detectMultiScale(gray_face)

        for (ex, ey, ew, eh) in eyes:
            #acid= predict(gray_face)
            acstr = predict(gray_face)

    cv2.imshow('Custom Face Recognition System', gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Quit if the key is Q
        #print("Accuracy is " + str(log.getAccuracy(acid)) + " % ")
        log.getAccuracyIndividual(acstr)
        #log.prepareLog(acid)
        log.flushAccuracy()
        break

cap.release()
cv2.destroyAllWindows()
