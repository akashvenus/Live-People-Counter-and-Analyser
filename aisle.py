import cv2 as cv
import numpy as np
import datetime
import mysql.connector
from centroid import CentroidTracker
from trackable import TrackableObject

Down1 = 0
Up1 = 0

Down2 = 0
Up2 = 0

def main():
    whT = 320
    confidenceThres = 0.4
    nmsThreshold = 0.3
    cap = cv.VideoCapture("test.mp4")
    cap2 = cv.VideoCapture("TestVideo.avi")


    classesFile = "coco-names.txt"
    classes = []
    with open(classesFile,'rt') as f:
        classes = f.read().rstrip('\n').split('\n')

    modelConfig = "yolov3-tiny.cfg"
    modelWeights = "yolov3-tiny.weights"

    net = cv.dnn.readNetFromDarknet(modelConfig,modelWeights)
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

    ct = CentroidTracker(maxDisappeared=40, maxDistance=50)
    trackers = []
    trackableObjects = {}


    def counting(objects):
        frameHeight = img.shape[0]
        frameWidth = img.shape[1]

        global Down1
        global Up1

        for (objectID, centroid) in objects.items():

            to = trackableObjects.get(objectID, None)

            if to is None:
                to = TrackableObject(objectID, centroid)

            else:

                y = [c[1] for c in to.centroids]
                direction = centroid[1] - np.mean(y)
                to.centroids.append(centroid)

                if not to.counted:

                    if direction < 0 and centroid[1] in range((frameHeight*17)//20 - 30, (frameHeight*17)//20 + 30):
                        Up1 += 1
                        to.counted = True

                    elif direction > 0 and centroid[1] in range((frameHeight*3)//20 - 30, (frameHeight*3)//20 + 30):
                        Down1 += 1
                        to.counted = True


            trackableObjects[objectID] = to
            cv.circle(img, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

        info = [
            ("Up", Up1),
            ("Down", Down1),
        ]

        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv.putText(img, text, (10, frameHeight - ((i * 20) + 20)),
                cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)


    def findObjects(outputs,img):
        hT,wT,cT = img.shape
        bbox = []
        classIds = []
        confs = []
        rects = []

        for output in outputs:
            for det in output:
                scores = det[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > confidenceThres:
                    w,h = int(det[2]*wT), int(det[3]*hT)
                    x,y = int((det[0]*wT) - w/2),int((det[1]*hT) - h/2)
                    bbox.append([x,y,w,h])
                    classIds.append(classId)
                    confs.append(float(confidence))

        indices = cv.dnn.NMSBoxes(bbox,confs,confidenceThres,nmsThreshold)
        for i in indices:
            i = i[0]
            box = bbox[i]
            x,y,w,h = box[0],box[1],box[2],box[3]
            if classes[classIds[i]].upper() == "PERSON":
                cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),thickness=2)
                cv.putText(img,f'{classes[classIds[i]].upper()} {int(confs[i]*100)}%',(x,y-10),cv.FONT_HERSHEY_SIMPLEX,
                0.6,(255,255,0),thickness = 2)
                rects.append((x,y,x+w,y+h))
                objects = ct.update(rects)
                counting(objects)
        x = datetime.datetime.now()
        cv.putText(img,f'{x.strftime("%x")}',(10,65),cv.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),thickness=2)
        cv.putText(img,f'{x.strftime("%X")}',(10,95),cv.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),thickness=2)


    def counting2(objects):
        frameHeight = img2.shape[0]
        frameWidth = img2.shape[1]

        global Down2
        global Up2

        for (objectID, centroid) in objects.items():

            to = trackableObjects.get(objectID, None)

            if to is None:
                to = TrackableObject(objectID, centroid)

            else:

                y = [c[1] for c in to.centroids]
                direction = centroid[1] - np.mean(y)
                to.centroids.append(centroid)

                if not to.counted:

                    if direction < 0 and centroid[1] in range((frameHeight*17)//20 - 30, (frameHeight*17)//20 + 30):
                        Up2 += 1
                        to.counted = True

                    elif direction > 0 and centroid[1] in range((frameHeight*3)//20 - 30, (frameHeight*3)//20 + 30):
                        Down2 += 1
                        to.counted = True


            trackableObjects[objectID] = to
            cv.circle(img2, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

        info = [
            ("Up", Up2),
            ("Down", Down2),
        ]

        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv.putText(img2, text, (10, frameHeight - ((i * 20) + 20)),
                cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)


    def findObjects2(outputs2,img2):
        hT,wT,cT = img2.shape
        bbox = []
        classIds = []
        confs = []
        rects = []

        for output in outputs2:
            for det in output:
                scores = det[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > confidenceThres:
                    w,h = int(det[2]*wT), int(det[3]*hT)
                    x,y = int((det[0]*wT) - w/2),int((det[1]*hT) - h/2)
                    bbox.append([x,y,w,h])
                    classIds.append(classId)
                    confs.append(float(confidence))

        indices = cv.dnn.NMSBoxes(bbox,confs,confidenceThres,nmsThreshold)
        for i in indices:
            i = i[0]
            box = bbox[i]
            x,y,w,h = box[0],box[1],box[2],box[3]
            if classes[classIds[i]].upper() == "PERSON":
                cv.rectangle(img2,(x,y),(x+w,y+h),(255,0,0),thickness=2)
                cv.putText(img2,f'{classes[classIds[i]].upper()} {int(confs[i]*100)}%',(x,y-10),cv.FONT_HERSHEY_SIMPLEX,
                0.6,(255,255,0),thickness = 2)
                rects.append((x,y,x+w,y+h))
                objects = ct.update(rects)
                counting2(objects)
        x = datetime.datetime.now()
        cv.putText(img2,f'{x.strftime("%x")}',(10,65),cv.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),thickness=2)
        cv.putText(img2,f'{x.strftime("%X")}',(10,95),cv.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),thickness=2)


    while(True):
        success,img = cap.read()
        frameHeight = img.shape[0]
        frameWidth = img.shape[1]
        cv.line(img, (0, (frameHeight*3) // 20), (frameWidth, (frameHeight*3) // 20), (255, 255, 255), 2)
        cv.line(img, (0, (frameHeight*17) // 20), (frameWidth, (frameHeight*17) // 20), (255, 255, 255), 2)
        blob = cv.dnn.blobFromImage(img,1/255,(whT,whT),[0,0,0],1,crop=False)
        net.setInput(blob)
        layerNames = net.getLayerNames()
        outputNames = [layerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]
        outputs = net.forward(outputNames)
        findObjects(outputs,img)
        resized = cv.resize(img,(550,550),interpolation = cv.INTER_AREA)
        success2,img2 = cap2.read()
        frameHeight2 = img2.shape[0]
        frameWidth2 = img2.shape[1]
        cv.line(img2, (0, (frameHeight2*3) // 20), (frameWidth2, (frameHeight2*3) // 20), (255, 255, 255), 2)
        cv.line(img2, (0, (frameHeight2*17) // 20), (frameWidth2, (frameHeight2*17) // 20), (255, 255, 255), 2)
        blob2 = cv.dnn.blobFromImage(img2,1/255,(whT,whT),[0,0,0],1,crop=False)
        net.setInput(blob2)
        layerNames2 = net.getLayerNames()
        outputNames2 = [layerNames2[i[0]-1] for i in net.getUnconnectedOutLayers()]
        outputs2 = net.forward(outputNames2)
        findObjects2(outputs2,img2)
        resized2 = cv.resize(img2,(550,550),interpolation = cv.INTER_AREA)
        Hori = np.concatenate((resized, resized2), axis=1)
        cv.imshow("Image",Hori)
        total1 = Up1+Down1
        total2 = Up2+Down2
        t = datetime.datetime.now()
        day = t.strftime("%Y-%m-%d")
        if cv.waitKey(20) & 0xFF==ord('d'):
            break

    cap.release()
    cv.destroyAllWindows()
    
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "root",
        database = "mydatabase"
    )

    mycursor = db.cursor()
    sql = "INSERT INTO aisles (A1, A2, Day) VALUES (%s, %s, %s)"
    val = (total1,total2,day)

    mycursor.execute(sql,val)

    db.commit()

    print(mycursor.rowcount, "record inserted.")

def work2():
    main()
