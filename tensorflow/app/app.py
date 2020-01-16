from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QFileDialog
from PIL.ImageQt import ImageQt
import cv2
import tensorflow as tf
import numpy as np
import os
from PIL import Image
from userprofile import User
from testWidget import test_widget
from design import Ui_MainWindow
import threading
import time
import re
import urllib.request
from PyQt5.QtWidgets import qApp
from utils import testdetection as vis_util
from utils import label_map_util
from utils import visualization_utils as vis_util
#Creates connections to firebase
sys.path.append("..")

userID = None #unique user id to identify in firebase
current_user = None #the current user
answer = None #to check if we retrieve anything from firebase
fname= None #file name for image
flag = True #flag to stop thread
fvideoname = None #video name
new_width = 800
new_height = 400
#Options to limit GPU uses
config = tf.ConfigProto()
config.gpu_options.allow_growth = True

#LOADING IN MODEL
MODEL_NAME = 'inference_graph_106k'

# Grab path to current working directory
CWD_PATH = '/home/do_duy_dao/TensorFlow/workspace/'

# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,'annotations','label_map.pbtxt')
   
# Number of classes the object detector can identify
NUM_CLASSES = 6
# Load the label map.
# Label maps map indices to category names, so that when our convolution
# Here we use internal utility functions, but anything that returns a
# dictionary mapping integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        od_graph_def.ParseFromString(fid.read())
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)

# Define input and output tensors (i.e. data) for the object detection classifier

# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# Each score represents level of confidence for each of the objects.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

#Creates UI and sets up connections for buttons
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.LoginButton.clicked.connect(self.login)
        self.ui.imagedetectbtn.clicked.connect(self.DetectImage)
        self.ui.openFilebtn.clicked.connect(self.openFile)
        self.ui.detectimage.clicked.connect(self.switchImageWidget)
        self.ui.detectvideo.clicked.connect(self.switchVideoWidget)
        self.ui.webcamDetect.clicked.connect(self.switchWebcamWidget)
        self.ui.logout.clicked.connect(self.switchLoginWidget)
        self.ui.detectCamera.clicked.connect(self.detectCameraIP)
        self.ui.detectCamera_2.clicked.connect(self.detectVideo)
        self.ui.openFilebtn_2.clicked.connect(self.openVideoFile)
        self.ui.homebutton.clicked.connect(self.switchHomeWidget)

#These set up the switches between the different pages for the application

    def switchHomeWidget(self):
        self.ui.stackedWidget_2.setCurrentWidget(self.ui.home_page) #page_6
        #self.ui.stackedWidget_4.setCurrentWidget(self.ui.page_4)

    def switchPasswordWidget(self):
        self.ui.stackedWidget_3.setCurrentWidget(self.ui.page_2)
        #self.ui.stackedWidget_4.setCurrentWidget(self.ui.page_4)

    def switchImageWidget(self):
        self.ui.label_21.setText("")
        self.ui.fileLabel.setText("Open file path")
      
        self.ui.stackedWidget_2.setCurrentWidget(self.ui.detect_image_page)
        #self.ui.stackedWidget_4.setCurrentWidget(self.ui.page_4)
    def switchWebcamWidget(self):
        self.ui.label_9.setText("")
        self.ui.stackedWidget_2.setCurrentWidget(self.ui.detect_webcam_page)
        #self.ui.stackedWidget_4.setCurrentWidget(self.ui.page_4)

    def switchVideoWidget(self):
        self.ui.errorvideo.setText("")
        self.ui.fileLabel_2.setText("Open file path")
        self.ui.stackedWidget_2.setCurrentWidget(self.ui.detect_video_page)
        #self.ui.stackedWidget_4.setCurrentWidget(self.ui.page_4)

    def switchLoginWidget(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.login_page)
        self.ui.stackedWidget_2.setCurrentWidget(self.ui.home_page) #page_6
        #self.ui.stackedWidget_4.setCurrentWidget(self.ui.page_5)
        self.ui.lineEdit_2.setText("")
        self.ui.listWidget_2.clear()
        self.ui.label_17.setText("")
        self.ui.fileLabel_2.setText("Open file path")
        self.ui.fileLabel.setText("Open file path")

        userID = None
        current_user = None
        answer = None
        fname= None
        f1= None
        flag = True

    #def signup(self):
        #global firebase
        #global flag
        #result = firebase.get('/users',None)
        #firstname = self.ui.firstnamelabel.text()
        #surname = self.ui.surnamelabel.text()
        #email = self.ui.emaillabel.text()
        #username = self.ui.usernamelabel.text()
        #password = self.ui.passwordlabel.text()
        #repassword = self.ui.passwordlabel2.text()


    #LETS THE USER Login
    def login(self):
        global answer
        global firebase
        global current_user
        global userID
        #result = firebase.get('/users',None)
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()

        #userID  = next((item for item in result if result[item]["username"] == username), None) #Get user ID
       	#answer  = next((item for item in result.values() if item["username"] == username), None) #Get user DATA

       	userID = 'dao'
       	answer = '1'
        if answer is None:
            self.ui.label_17.setText("User doesn't exist")
        else:
            if answer == password:
                current_user = userID
                #firebase.post('/users/'+ userID + '/imagePaths','C:/Users/abdsaam/Desktop/pythonapp/designs/images/greentick.png')
                self.ui.stackedWidget.setCurrentIndex(0)

                qApp.processEvents()
                if "imagePaths" in answer:
                    for x in answer["imagePaths"].values():
                        print(x)
                        #imageBlob = bucket.blob(current_user + "/" + x) #Get the users folder from database, and their images
                        print(imageBlob.public_url)
                        with urllib.request.urlopen(imageBlob.public_url) as url:
                            s = url.read()
                            wid = test_widget()
                            wid.setImage(s)
                            values = x.split()

                            widgetItem = QtWidgets.QListWidgetItem(self.ui.listWidget_2)
                            widgetItem.setSizeHint(wid.sizeHint())
                            self.ui.listWidget_2.addItem(widgetItem)
                            self.ui.listWidget_2.setItemWidget(widgetItem,wid)

            else:
                self.ui.label_17.setText("Incorrect password")

    def openFile(self):
        global fname
        fname = QFileDialog.getOpenFileName(None,'Open image files (*.jpg *.png)')
        pixmap = QtGui.QPixmap(fname[0])
        scaled_pixmap = pixmap.scaled(500,500,QtCore.Qt.KeepAspectRatio)
        self.ui.label_11.setPixmap(QtGui.QPixmap(scaled_pixmap))
        self.ui.fileLabel.setText(fname[0])

	
    def DetectImage(self):
        self.ui.label_21.setText("Loading.... Application might freeze....")
        qApp.processEvents()
        global fname

        image= cv2.imread(fname[0])
        image_expanded = np.expand_dims(image, axis=0) #convert to numpy array
        #Saves model output into 4 values
        (boxes, scores, classes, num) = sess.run([detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: image_expanded}) 
        # Draw the results of the detection (aka 'visulaize the results')

        vis_util.visualize_boxes_and_labels_on_image_array(
            image,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=3,
            min_score_thresh=0.6)

       	showInMovedWindow('Detec image',image, 1100, 240)
		
        #cv2.imshow('Object detector', image)
    def openVideoFile(self):
        global fvideoname
        fvideoname = QFileDialog.getOpenFileName(None,'Open video files (*.mp4 *.mov)')
        self.ui.fileLabel_2.setText(fvideoname[0])
     
    def detectVideo(self):
        global fvideoname
        self.ui.errorvideo.setText("Loading.... Application might freeze....")
        qApp.processEvents()
        video = cv2.VideoCapture(fvideoname[0])

        if video.isOpened():
            self.ui.errorvideo.setText("Done!")
            while(video.isOpened()):
                #Get frame and expand it so it can fed to tensorflow
                ret, frame = video.read()
                frame_expanded = np.expand_dims(frame, axis=0)
                # Perform the actual detection by running the model with the image as input
                (boxes, scores, classes, num) = sess.run(
                    [detection_boxes, detection_scores, detection_classes, num_detections],
                    feed_dict={image_tensor: frame_expanded})
                #Draws bounding box around the detected part of the image #Helper code
                vis_util.visualize_boxes_and_labels_on_image_array(
                    frame,
                    np.squeeze(boxes),
                    np.squeeze(classes).astype(np.int32),
                    np.squeeze(scores),
                    category_index,
                    use_normalized_coordinates=True,
                    line_thickness=3,
                    min_score_thresh=0.6)

                #Show the detected video on the window
                #cv2.imshow("Detec video", frame)
                showInMovedWindow('Detec video',frame, 200, 140)
                #Q or Esc to quit detecting webcam
                k = cv2.waitKey(1)
                if k == ord('q') or k == 27:
                    break
                if cv2.getWindowProperty("Detec video",1) == -1:
                    break
            	
            # Clean up
            video.release()
            cv2.destroyAllWindows()
 
        else:
            self.ui.errorvideo.setText("Error with video file")

    def detectCameraIP(self):

        self.ui.label_9.setText("Loading.... Application might freeze....")
        qApp.processEvents()
       
        video = cv2.VideoCapture(0)
        ret = video.set(3,1280)
        ret = video.set(4,720)

        if video.isOpened():
            self.ui.label_9.setText("Done!")
            current_time = time.time()
            while(True):
                #Get frame and expand it so it can fed to tensorflow
                ret, frame = video.read()

                frame_expanded = np.expand_dims(frame, axis=0)
                # Perform the actual detection by running the model with the image as input
                (boxes, scores, classes, num) = sess.run(
                    [detection_boxes, detection_scores, detection_classes, num_detections],
                    feed_dict={image_tensor: frame_expanded})

                #Draws bounding box around the detected part of the image #Helper code
                vis_util.visualize_boxes_and_labels_on_image_array(
                    frame,
                    np.squeeze(boxes),
                    np.squeeze(classes).astype(np.int32),
                    np.squeeze(scores),
                    category_index,
                    use_normalized_coordinates=True,
                    line_thickness=3,
                    min_score_thresh=0.6)

                #Show the detected image on the window
                showInMovedWindow('Detec video',frame, 0, 0) #200, 140
                #Q or Esc to quit detecting webcam
                k = cv2.waitKey(1)
                if k == ord('q') or k == 27:
                    break

            # Clean up
            video.release()
            cv2.destroyAllWindows()
        else:
            self.ui.label_9.setText("Cannot find camera")
# set up pos for window detec
def showInMovedWindow(winname, img, x, y):
	    cv2.namedWindow(winname)        # Create a named window
	    cv2.moveWindow(winname, x, y)   # Move it to (x,y)
	    cv2.imshow(winname,img)	

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
exit(app.exec_())