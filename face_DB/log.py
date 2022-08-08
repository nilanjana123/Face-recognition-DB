import sqlite3
import re

def getFace(ID):
    conn = sqlite3.connect("people.db")
    cmd = "select * from fdb2 where id=" + str(ID)
    cursor = conn.execute(cmd)
    profile = None
    for row in cursor:
        profile=row
    conn.close()
    return profile

def createLog(id,total,success):
    conn5 = sqlite3.connect("people.db")
    cmd5 = "insert into face_log2 (id,total,success) values(" + str(id) + "," + str(total)+","+str(success)+")"
    conn5.execute(cmd5)
    conn5.commit()
    conn5.close()

def getAccuracy(ID):
    conn = sqlite3.connect("people.db")
    cmd = "select * from accuracy where id =" + str(ID)
    cmd2 = "select * from accuracy"
    cursor = conn.execute(cmd)
    cursor2 = conn.execute(cmd2)
    count = 0
    count2 = 0
    for row in cursor:
        count = count + 1
    for row in cursor2:
        count2 = count2 + 1
    conn.close()
    accuracy = 0
    if(count2 > 0):
        accuracy = (count/count2)*100
    return accuracy



def getAccuracyIndividual(acstr):
    faceArr = re.findall('\d+', acstr)

    conn = sqlite3.connect("people.db")

    cmd2 = "select * from accuracy"
    cursor2 = conn.execute(cmd2)
    count2 = 0
    for row in cursor2:
        count2 = count2 + 1

    print("The results for recognition are : \n")

    for face in faceArr:
        cmd = "select * from accuracy where id =" + str(face)
        cursor = conn.execute(cmd)
        count = 0
        for row in cursor:
            count = count + 1
        accuracy = 0
        if (count2 > 0):
            accuracy = (count / count2) * 100

        accuracy = "%.2f" % accuracy

        print("Accuracy of " + str(getFace(face)[1]) + " (id = " + face + ") is " + str(accuracy) + "%.")
    conn.close()


def flushAccuracy():
    conn3 = sqlite3.connect("people.db")
    cmd3 = "delete from accuracy"
    conn3.execute(cmd3)
    conn3.commit()
    conn3.close()

def prepareLog(ID):
    conn = sqlite3.connect("people.db")
    cmd = "select * from accuracy where id =" + str(ID)
    cmd2 = "select * from accuracy"
    cursor = conn.execute(cmd)
    cursor2 = conn.execute(cmd2)
    success = 0
    total = 0
    for row in cursor:
        success = success + 1
    for row in cursor2:
        total = total + 1
    conn.close()
    flushAccuracy()
    createLog(ID, total, success)