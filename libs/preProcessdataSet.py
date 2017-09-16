import os
import shutil
import cv2
import numpy as np
pathPrefix = "./unlabeled/"


def renameAll():
    count = 0
    for x,y,z in os.walk(pathPrefix):
        for name in z:
            if name[-4:] in [".png",".jpg"]:
                path = os.path.join(x , name)
                print(path)
                count +=1
                shutil.move(path,pathPrefix + "table_tennis_ball_{0}{1}".format(count,name[-4:]))
            else:
                print(name[:-4])
def resize():
    destsize= 512
    for x,y,z in os.walk(pathPrefix):    
        for name in z:
            if name[-4:] in [".png",".jpg"]:
                path = os.path.join(x , name)
                img = cv2.imread(path)                        
                s = img.shape
                if(s[0] > s[1]):
                    img_d = cv2.resize(img,dsize = (0,0),fx = destsize/s[0],fy = destsize/s[0])
                    img_temp = np.zeros(shape = (destsize,destsize,3),dtype=np.uint8)
                    sd = img_d.shape
                    img_temp[0:sd[0],0:sd[1],0:sd[2]]=img_d
                    cv2.imwrite(path,img_temp)
                else:
                    img_d = cv2.resize(img,dsize = (0,0),fx = destsize/s[1],fy = destsize/s[1])
                    img_temp = np.zeros(shape = (destsize,destsize,3),dtype=np.uint8)
                    sd = img_d.shape
                    img_temp[0:sd[0],0:sd[1],0:sd[2]]=img_d
                    cv2.imwrite(path,img_temp)     
resize()               
