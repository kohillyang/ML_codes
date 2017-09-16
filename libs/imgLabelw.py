import os
import sys
import cv2
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import logging
import random
logging.basicConfig(level=logging.DEBUG, 
                    format='[%(levelname)s]'
                           '-[%(lineno)d] :  %(message)s')
    
class LabelWidget(QWidget):
    def __init__(self, imgs):
        super(LabelWidget,self).__init__()    
        self.imgs  = imgs

        if len(self.imgs) ==0 :
            logging.warning("there is no imgs to label in that folder.")
            sys.exit(-1)
        self.img_index = 0
        self.imgFilePath = self.imgs[self.img_index]
        self.scale = 3
        self.loadImg(self.imgFilePath)
        img = self.img
        self.setFixedSize(QSize(img.width() ,img.height()))
        self.isDrawing = False
        try:
            self.loadRect(self.imgFilePath,True)
        except FileNotFoundError:
            self.startPos = QPointF(0,0)
            self.endPos = QPointF(0,0)            
        self.setFocusPolicy(Qt.ClickFocus)
    def paintEvent(self,event):
        painter = QPainter()
        painter.begin(self)
        painter.drawImage(QPoint(0,0),self.img)
        painter.setPen(QPen(QColor(0, 255, 0, 128)))
        painter.drawRect(QRectF(self.startPos,self.endPos))
        
        painter.end()

    def mouseReleaseEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            self.isDrawing = False
            self.endPos = ev.pos()
        self.repaint()
    def mousePressEvent(self,ev):
        if ev.button() == Qt.LeftButton:
            self.startPos = ev.pos()
            self.endPos = self.startPos
            self.isDrawing = True
        self.repaint()
    def mouseMoveEvent(self, ev):
        if self.isDrawing:
            self.endPos = ev.pos()
        self.repaint()
    def loadImg(self,filePath):
        img = QImage(QImage(filePath))
        width,height = img.width(),img.height()
        self.img = img.scaled(QSize(int(width * self.scale),int(height * self.scale)),Qt.KeepAspectRatio)        
    @staticmethod
    def labelFilePath(imgFilePath):
        return os.path.splitext(imgFilePath)[0] + ".label" 
    def loadRect(self,imgFilePath,raiseNotFound = False):
        try:
            r = open(self.labelFilePath(imgFilePath),"rt").read().strip().split(" ")
            r = list(map(lambda x:float(x) * self.scale,r))
            self.startPos = QPointF(r[0],r[1])
            self.endPos = QPointF(r[2],r[3])    
        except FileNotFoundError as e:
            logging.debug("no label file {0}".format(imgFilePath))
            if raiseNotFound:
                raise e
    def saveRect(self,imgFilePath):
        with open(self.labelFilePath(imgFilePath),"wt") as f:
            f.write("%f %f %f %f"%(self.startPos.x()/self.scale,
                                    self.startPos.y()/self.scale,
                                    self.endPos.x()/self.scale,
                                    self.endPos.y()/self.scale))
    def keyPressEvent(self,ev):
        key = ev.key()
        if key == 16777223:
            self.startPos = QPointF(0,0)
            self.endPos = QPointF(0,0)
        if key== Qt.Key_D:
            self.saveRect(self.imgFilePath)
            try:
                self.img_index += 1
                self.img_index %= len(self.imgs)
                self.imgFilePath = self.imgs[self.img_index]

                self.loadRect(self.imgFilePath)
                self.loadImg(self.imgFilePath)
            except IndexError as e:
                logging.debug("Have no imgs(right).")
        if key== Qt.Key_A:
            self.saveRect(self.imgFilePath)
            try:
                self.img_index -= 1
                self.img_index %= len(self.imgs)
                self.imgFilePath = self.imgs[self.img_index]
                
                self.loadRect(self.imgFilePath)
                self.loadImg(self.imgFilePath)
            except IndexError as e:
                logging.debug("Have no imgs(Left).")
        if key == Qt.Key_Left:
            self.startPos -= QPointF(1,0)
            self.endPos -= QPointF(1,0)                
        if key == Qt.Key_Up:
            self.startPos -= QPointF(0,1)
            self.endPos -= QPointF(0,1)                
        if key == Qt.Key_Right:
            self.startPos += QPointF(1,0)
            self.endPos += QPointF(1,0)                
        if key== Qt.Key_Down:
            self.startPos += QPointF(0,1)
            self.endPos += QPointF(0,1)                
        self.repaint()        
        logging.info("%d"%(len(self.imgs)))
        self.update()
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__()
        if len(sys.argv) > 1:
            self.imgFolder = sys.argv[1]        
        else:
            self.imgFolder = "./car_data/labeled/"
            # self.imgFolder = "./imgs/"
        self.imgs = []
        for x,y,z in os.walk(self.imgFolder):
            for name in z:
                path = x + name
                if path[-4:] in ['.png','.jpg']:
                    self.imgs.append(path)
        # self.imgs.sort(key=str.lower)
        random.shuffle(self.imgs)
        centerWidget = LabelWidget(self.imgs)
        self.setCentralWidget(centerWidget)
def checkLabels(fileDir):
    fileList = []
    for x,y,z in os.walk(fileDir):
        for name in z:
            path = x + name
            if path[-4:] in ['.png','.jpg']:
                fileList.append(path)
    for fpath in fileList:
        labelFilePath = LabelWidget.labelFilePath(fpath)
        img  = cv2.imread(fpath)
        xmin,ymin,xmax,ymax = map(lambda x:int(float(x)),open(labelFilePath,"rt").read().strip().split(" "))
        img = cv2.rectangle(img,(xmin, ymin),(xmax,ymax),(0,255,0),3)  
        cv2.imshow("result",img)
        cv2.waitKey(0) 
if __name__ == "__main__":
    # checkLabels(sys.argv[1])
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()    
    sys.exit(app.exec_())