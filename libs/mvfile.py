import os
import shutil
fileList = []
for x,y,z in os.walk("./unlabeled/"):
    for name in z:
        fileList.append(os.path.join(x,name))
for filePath in fileList:
    if filePath[-4:] in [".png",".jpg"] and filePath[:-4] + ".label" in fileList:
        shutil.move(filePath,"./labeled/")
        shutil.move(filePath[:-4] + ".label","./labeled/") 