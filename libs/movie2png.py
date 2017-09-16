filePrefix="table_tennis_ball2from_vedios"
import cv2,os
filelist = []
for x,y,z in os.walk("./videos/"):
    for name in z:
        path = os.path.join(x,name)
        if name.endswith(".mp4"):
            filelist.append(path)
for videofile in filelist:
    vi = cv2.VideoCapture(videofile)
    count = 0
    while True:
        r,img = vi.read()
        if not r:
            break
        count +=1
        cv2.imwrite("./unlabeled/{1}_{0}.png".format(count,filePrefix),img)