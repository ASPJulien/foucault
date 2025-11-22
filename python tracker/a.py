# tracking avec transformée de hough
# https://docs.opencv.org/4.12.0/dd/d1a/group__imgproc__feature.html#ga47849c3be0d0406ad3ca45db65a25d2d
import numpy as np
import cv2 as cv
import csv
valeurs = []

nbe = 0

def circledetector(img, current_frame):
    global nbe
    global valeurs
    #img = cv.imread('C:/Users/Julie/Pictures/b.png', cv.IMREAD_GRAYSCALE)
    #cv.imshow('frame', img)
    assert img is not None, "image non lue"
    img = cv.medianBlur(img,3)
    cimg = cv.cvtColor(img,cv.COLOR_GRAY2BGR)

    circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT_ALT,
                              dp=2, # diviseur de la resolution de l'image
                              minDist=500, # distance entre 2 cercles détectés
                              param1=300,param2=0.95, # param1: magic value, param2: % de parfaititude du cercle
                              minRadius=10,maxRadius=0) # trivial par réccurence immédiate
    try:
        if circles is not None and len(circles[0]) == 1:
            for i in circles[0,:]:
                valeurs.append([current_frame,i[0], i[1]])
                i =  np.int16(i)
                cv.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
                cv.circle(cimg,(i[0],i[1]),2,(0,0,255),2)
        else:
            nbe +=1
            print(f"grosse grosse galere: {nbe} à la frame {current_frame}")
    #print("a")
    except:
        nbe +=1
        print(f"grosse grosse galere: {nbe} à la frame {current_frame}")
    #return cimg
    return None
    #cv.destroyAllWindows()


cap = cv.VideoCapture('C:/Users/Julie/Videos/Img 0002(2).mp4')
print("nombre de frames à traiter:", int(cap.get(cv.CAP_PROP_FRAME_COUNT)))
while cap.isOpened():
    lu, frame = cap.read()
    if not lu:
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    current_frame = int(cap.get(cv.CAP_PROP_POS_FRAMES)) - 1 # -1 à cause du read

    #cv.imshow('frame', gray)
    #cv.imshow('frame', circledetector(gray, current_frame))
    circledetector(gray, current_frame)
    if cv.waitKey(1) == ord('q'):
        break # behhhh prend ça XX
print(f"Lecture finie: {int(cap.get(cv.CAP_PROP_FRAME_COUNT))-nbe}/{int(cap.get(cv.CAP_PROP_FRAME_COUNT))} frames traitées, {(int(cap.get(cv.CAP_PROP_FRAME_COUNT))-nbe)/int(cap.get(cv.CAP_PROP_FRAME_COUNT))}%")
cap.release()
cv.destroyAllWindows()

csv_filename = 'simsim.csv'
with open(csv_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Frame', 'X', 'Y']) # header
    writer.writerows(valeurs) # valeurs

