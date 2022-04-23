import sys
from PyQt5.QtCore import QRect, QSize, pyqtSlot
from PyQt5.QtWidgets import QApplication,QLabel, QLineEdit, QListWidget, QMainWindow, QPushButton, QWidget,QComboBox,QListWidgetItem,QMessageBox
from google_speech import Speech
from PyQt5.QtGui import QPixmap
import urllib.parse
import requests
import time

#Class to make the GUI with PyQT5
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_api = "https://www.mapquestapi.com/directions/v2/route?"#api site
        self.key = "1TvUJEZQVdbj7gikUoNgfUemKXcOlIUj"#api key
        self.Pathss = ["Fastest","Shortest","Pedestrian","Bicycle"] #Choose path
        self.Avoidss = ["Highways","Toll Road","Ferry","Unpaved","Approximate Seasonal Closure","Country Border Crossing","Bridge","Tunnel"]
        self.Distances = ["KM","Mi","M"]
        self.setWindowTitle("Map Quest")#sets gui title
        self.IMAGES = ["mapquest.jpg","welcome","Right","Left","Straight"]#array of images
        self.Image = self.IMAGES[0]#stock image
        self.setFixedSize(QSize(600,800))#size of window
        self.Create()#creates buttons and resizes and moves it.
        self.Lock.clicked.connect(self.Start)#connection of Start
        self.Exit.clicked.connect(self.Exi)#connnection of exit button
        self.Text_Label.clicked.connect(self.Clear_List)#Clear button
        self.show()
    def Create(self):
        self.pixmap = QPixmap(self.Image)
        self.Next = QPushButton("NEXT!",self)
        self.Lock = QPushButton("START",self)
        self.Exit = QPushButton("EXIT",self)
        self.Image_Label = QLabel(self)
        self.Text_Label = QPushButton("CLEAR",self)
        self.orig = QLineEdit(self)
        self.dest = QLineEdit(self)
        self.Logs = QListWidget(self)
        self.Logs.setGeometry(305,0,290,500)
        self.orig.setPlaceholderText("Original Location")
        self.dest.setPlaceholderText("Destination")
        self.Image_Label.setPixmap(self.pixmap)
        self.Image_Label.resize(300,300)
        self.Next.resize(200,200)
        self.Lock.resize(200,200)
        self.Exit.resize(200,200)
        self.Text_Label.resize(200,30)
        self.Move()
    def Move(self):
        self.Image_Label.move(0,100)
        self.Text_Label.move(200,555)
        self.Next.move(0,605)
        self.Lock.move(200,605)
        self.Exit.move(400,605)
        self.Combo()
    def Combo(self):
        self.Paths = QComboBox(self)
        self.Paths.addItems(self.Pathss)
        self.Avoids = QComboBox(self)
        self.Avoids.addItems(self.Avoidss)
        self.Distance = QComboBox(self)
        self.Distance.addItems(self.Distances)
        self.Paths.setGeometry(20,520,100,20)
        self.Avoids.setGeometry(120,520,100,20)
        self.Distance.setGeometry(220,520,100,20)
        self.orig.setGeometry(340,520,120,20)
        self.dest.setGeometry(470,520,120,20)
    
    @pyqtSlot()#signal and slots
    def Start(self):
        self.url = self.main_api + urllib.parse.urlencode({"key":self.key, "from":self.orig.text(), "to":self.dest.text(),"routeType":self.Paths.currentText(),"avoids":self.Avoids.currentText()},safe=",")
        print(self.url)
        self.json_data = requests.get(self.url).json()
        self.json_status = self.json_data["info"]["statuscode"]
        self.Error_Codes()
    def Error_Codes(self):#main functionality
        print (self.json_status)
        if self.json_status == 0:
            self.Logs.addItem("API Status:"+str(self.json_status)+"=A successful route call.")
            self.Logs.addItem("=============================================")
            self.Logs.addItem("Directions from " + (self.orig.text()) + " to " + (self.dest.text()))
            self.Logs.addItem("Trip Duration:   " + (self.json_data["route"]["formattedTime"]))#appends items to QWidgetList
            if self.Distance.currentText() == "KM":
                self.Logs.addItem("Kilometers:      " + str("{:.2f}".format((self.json_data["route"]["distance"])*1.61) + "KM"))
            elif self.Distance.currentText() == "M":
                self.Logs.addItem("Meters:      " + str("{:.2f}".format(((self.json_data["route"]["distance"])*1.61)*1000) + "M"))
            else:
                self.Logs.addItem("Miles:      " + str("{:.2f}".format(((self.json_data["route"]["distance"])*1.61)*.621371) +"MI"))
            self.Logs.addItem("Fuel Used (Ltr): " + str("{:.2f}".format((self.json_data["route"]["fuelUsed"])*3.78)))
            self.Logs.addItem("=============================================")
            if self.Distance.currentText() == "KM":
                for each in self.json_data["route"]["legs"][0]["maneuvers"]:
                    self.ImageChange(each)#Changes Image
                    self.Information((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + self.Distance.currentText()+ ")"))
                    self.Logs.addItem((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + self.Distance.currentText()+ ")"))
            elif self.Distance.currentText() == "M":
                for each in self.json_data["route"]["legs"][0]["maneuvers"]:
                    self.ImageChange(each)
                    self.Information((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61*1000) + self.Distance.currentText() + ")"))
                    self.Logs.addItem((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61*1000) + self.Distance.currentText() + ")"))
            else:
                for each in self.json_data["route"]["legs"][0]["maneuvers"]:
                    self.ImageChange(each)
                    self.Information((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61*.621371) + self.Distance.currentText()+ ")"))
                    self.Logs.addItem((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61*.621371) + self.Distance.currentText()+ ")"))
            self.Logs.addItem("Fuel Used (Ltr): " + str("{:.2f}".format((self.json_data["route"]["fuelUsed"])*3.78)))
            self.Logs.addItem("=============================================\n")
        elif self.json_status == 400:
            self.msgBox = QMessageBox()#Dialog Box, also preventing the crash of GUI
            self.Logs.addItem("Clearing List!")
            self.msgBox.setIcon(QMessageBox.Warning)
            self.msgBox.setText("There are no routes available here.")
            self.msgBox.setWindowTitle("ERROR!!")
            self.msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            returnValue = self.msgBox.exec()
            self.Logs.clear()
        else:
            self.msgBox2 = QMessageBox()
            self.Logs.addItem("Clearing List!")
            self.msgBox2.setIcon(QMessageBox.Warning)
            self.msgBox2.setText("Go to the documentation for the error.")
            self.msgBox2.setWindowTitle("ERROR!!")
            self.msgBox2.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            returnValue = self.msgBox2.exec()
            self.Logs.clear()
    @pyqtSlot()
    def Exi(self):
        self.close()
    
    @pyqtSlot()
    def Clear_List(self):
        self.Logs.clear()
        
    def Information(self,text):
        self.msgBox3 = QMessageBox()
        self.msgBox3.setIcon(QMessageBox.Information)
        self.msgBox3.setText(text)
        self.msgBox3.setWindowTitle("Direction")
        self.msgBox3.setStandardButtons(QMessageBox.Ok)
        lang = "en"
        speech = Speech(text, lang)
        returnValue = self.msgBox3.exec()
        speech.play()
        
    def ImageChange(self,yea):
        print(yea["narrative"])
        if "right" in (yea["narrative"]):
            self.pixmap = QPixmap(self.IMAGES[2])
            self.Image_Label.setPixmap(self.pixmap)
        elif "left" in (yea["narrative"]):
            self.pixmap = QPixmap(self.IMAGES[3])
            self.Image_Label.setPixmap(self.pixmap)
        elif "straight" in (yea["narrative"]):
            self.pixmap = QPixmap(self.IMAGES[4])
            self.Image_Label.setPixmap(self.pixmap)
        elif "welcome" in (yea["narrative"]) or "Welcome" in (yea["narrative"]):
            self.pixmap = QPixmap(self.IMAGES[1])
            self.Image_Label.setPixmap(self.pixmap)
        else:
            self.pixmap = QPixmap(self.IMAGES[0])
            self.Image_Label.setPixmap(self.pixmap)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    Window = MainWindow()
    sys.exit(app.exec())
