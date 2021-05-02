import cv2 as cv
import numpy as np
import datetime
import mysql.connector
from centroid import CentroidTracker
from trackable import TrackableObject

totalDown = 0
totalUp = 0

def main():
    whT = 320
    confidenceThres = 0.4
    nmsThreshold = 0.3
    cap = cv.VideoCapture("TestVideo.avi")


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
    store = []

    def counting(objects):
        frameHeight = img.shape[0]
        frameWidth = img.shape[1]

        global totalDown
        global totalUp

        for (objectID, centroid) in objects.items():

            to = trackableObjects.get(objectID, None)

            if to is None:
                to = TrackableObject(objectID, centroid)

            else:

                y = [c[1] for c in to.centroids]
                direction = centroid[1] - np.mean(y)
                to.centroids.append(centroid)

                if not to.counted:

                    if direction < 0 and centroid[1] in range(frameHeight//2 - 30, frameHeight//2 + 30):
                        totalUp += 1
                        to.counted = True

                    elif direction > 0 and centroid[1] in range(frameHeight//2 - 30, frameHeight//2 + 30):
                        t = datetime.datetime.now()
                        totalDown += 1
                        temp = (totalDown,t.strftime("%X"),t.strftime("%Y-%m-%d"))
                        store.append(temp)
                        to.counted = True


            trackableObjects[objectID] = to
            cv.circle(img, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

        info = [
            ("Up", totalUp),
            ("Down", totalDown),
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


    while(True):
        success,img = cap.read()

        frameHeight = img.shape[0]
        frameWidth = img.shape[1]
        cv.line(img, (0, frameHeight // 2), (frameWidth, frameHeight // 2), (0, 255, 255), 2)

        blob = cv.dnn.blobFromImage(img,1/255,(whT,whT),[0,0,0],1,crop=False)
        net.setInput(blob)
        layerNames = net.getLayerNames()
        outputNames = [layerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]
        outputs = net.forward(outputNames)
        findObjects(outputs,img)
        resized = cv.resize(img,(550,550),interpolation = cv.INTER_AREA);
        cv.imshow("Front",resized)
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
    sql = "INSERT INTO details (count, InTime, Day) VALUES (%s, %s, %s)"

    mycursor.executemany(sql, store)

    db.commit()

    print(mycursor.rowcount, "was inserted.")

def work():
    main()
