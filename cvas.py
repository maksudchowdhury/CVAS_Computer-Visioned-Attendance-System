import cv2
import numpy as np
import face_recognition as fr
import os
from datetime import datetime

unknownStud=0
def folderCreate(attendanceDocmentFoldername):
    FileTime = datetime.now()
    currentDate = FileTime.strftime("%d-%m-%Y-(%I;%M;%S %p)")
    Filename=currentDate+"_Attendance.csv"

    attendanceDocmentFilePath = os.path.join(
        attendanceDocmentFoldername, Filename)
    
    attendanceFile = open(attendanceDocmentFilePath, "w")
    attendanceFile.writelines('Name,id,Time')
    attendanceFile.close()
    return attendanceDocmentFilePath


def findEncoding(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList



#resizing Source Attendance Image
def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def markAttendance(name,id, openDocFilePath):
    
    with open(openDocFilePath, 'r+')as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name == 'Unknown':
            global unknownStud 
            unknownStud += 1

            now = datetime.now()
            dtstring = now.strftime('%H:%M:%S')
            unknownStudNo=str(unknownStud)
            f.writelines(f'\n{name+" "+unknownStudNo},{id},{dtstring}')

        elif name not in nameList:
            now = datetime.now()
            dtstring = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{id},{dtstring}')

def cvasMain():
    setWindowWidth = 2160
    sourceImageFolderName = 'SourceImages'
    screenShotfolderName = 'Attendance Image'
    attendaceCheckingImageFile = screenShotfolderName+'/ss1.jpg'
    attendanceDocmentFoldername = 'Attendance Document/'
  

    path = sourceImageFolderName
    images = []
    studentNames = []
    studentID = []
    myList = os.listdir(path)
    name = 'Unknown'
    id='n/a' 
    for imgName in myList:
        currentImage = cv2.imread(f'{path}/{imgName}')
        images.append(currentImage)
        name_ID = os.path.splitext(imgName)[0]
        studName = name_ID.split('_')[0]
        studentNames.append(studName)
        studID = name_ID.split('_')[1]
        studentID.append(studID)


    encodeListKnown = findEncoding(images)


    fullImage = cv2.imread(attendaceCheckingImageFile)
    capturedFaces = ResizeWithAspectRatio(fullImage, width=setWindowWidth)


    facesCurFrame = fr.face_locations(capturedFaces)
    encodeCurFrame = fr.face_encodings(capturedFaces, facesCurFrame)


    #attendance name Listing func


    openDocFilePath = folderCreate(attendanceDocmentFoldername)


    #Identifying and boxing then attendace writing
    folderCreate(attendanceDocmentFoldername)
    for encodeFace, faceloc in zip(encodeCurFrame, facesCurFrame):
        matches = fr.compare_faces(encodeListKnown, encodeFace)
        faceDis = fr.face_distance(encodeListKnown, encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = studentNames[matchIndex].upper()
            id = studentID[matchIndex].upper()
            print(name)
        y1, x2, y2, x1 = faceloc
        cv2.rectangle(capturedFaces, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.rectangle(capturedFaces, (x1, y2-25),
                      (x2, y2), (0, 255, 0), cv2.FILLED)
        cv2.putText(capturedFaces, name, (x1+6, y2-6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        markAttendance(name, id, openDocFilePath)

    cv2.imshow('Attendance', capturedFaces)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)

check=folderCreate('Attendance Document/')
