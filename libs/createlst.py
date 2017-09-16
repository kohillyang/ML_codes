import cv2,os,sys
if len(sys.argv) > 2:
    rootPath = sys.argv[1] 
    lstPath = sys.argv[2]
else:
    print('''
Usage:
    python3 creatlst.py labledPath lstPath
    format: xmin,ymin,xmax,ymax
    ''')
    sys.exit(-1)
img_paths = []
for x,y,z in os.walk(rootPath):
    for name in z:
        path = os.path.join(x,name)    
        if path[-4:] in [".png",".jpg"]:
            img_paths.append(path)

with open(lstPath,"wt") as f1:            
    for index,filePath in  enumerate(img_paths) :
        with open(filePath[:-4] + ".label","rt") as f:
            img = cv2.imread(filePath)
            xmin,ymin,xmax,ymax = map(lambda x:float(x),f.read().strip().split(" "))
            if xmin > xmax:
                tmp = [xmin,ymin]
                xmin,ymin = [xmax,ymax]
                xmax,ymax = tmp
            xmin /= img.shape[1]
            xmax /= img.shape[1]
            ymin /= img.shape[0]
            ymax /= img.shape[0]
    #             f1.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\n".format(
    #                 index,2,5,img.shape[0],img.shape[1],index + 1,
    #                 xmin,ymin,xmax,ymax,filePath[19:]))
            try:
                assert xmax > xmin
                assert ymax > ymin
                f1.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\n".format(
                    index,
                    2,5,0,xmin,ymin,xmax,ymax,
                    os.path.basename(filePath)))
                print(filePath)
            except AssertionError:
                print(xmin*img.shape[1],xmax*img.shape[1])
                print(ymin*img.shape[0],ymax*img.shape[0])