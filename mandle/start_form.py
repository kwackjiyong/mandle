
from PyQt5 import QtCore, QtGui, QtWidgets
from src.run import mandle_run
from view.option import Option_Form
import sys
import json
class Ui_MainWindow(object):
    excute_form = 0
    def jsonRead(self):
        with open("data.json", "r") as data_json:
            resultset = json.load(data_json)
            return resultset
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(312, 130)
        MainWindow.setFixedSize(312, 130)
        #MainWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 10, 141, 71))
        font = QtGui.QFont()
        font.setFamily("야놀자 야체 R")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(160, 10, 141, 71))
        font = QtGui.QFont()
        font.setFamily("야놀자 야체 R")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")


        #메인 윈도우 부분
        MainWindow.setCentralWidget(self.centralwidget)
        
        #메뉴바
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 312, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)

        #상태바
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        #메뉴추가
        self.actionDddfds = QtWidgets.QAction(MainWindow)
        self.actionDddfds.setObjectName("actionDddfds")
        self.menu.addAction(self.actionDddfds)
        #메뉴액션들 추가
        self.menubar.addAction(self.menu.menuAction())
        #컴포넌트 내용 삽입
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #액션 연동
        self.pushButton_2.clicked.connect(self.excute_pro)
        self.pushButton_3.clicked.connect(self.exit_pro)
        self.actionDddfds.triggered.connect(self.option_exec)
    #컴포넌트 텍스트 삽입    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "맨들 - Motion Handler"))
        MainWindow.setWindowIcon(QtGui.QIcon("view/icon2.png"))
        self.pushButton_2.setText(_translate("MainWindow", "실행"))
        self.pushButton_3.setText(_translate("MainWindow", "종료"))
        self.menu.setTitle(_translate("MainWindow", "옵션"))
        self.actionDddfds.setText(_translate("MainWindow", "동작설정"))
    #설정위젯 실행
    def option_exec(self):
        wind = Option_Form()
        wind.showModal()
    
    #실행버튼
    def excute_pro(self):
        print(self.excute_form)
        if self.excute_form == 0:
            self.excute_form = 1
            print('excute')
            _translate = QtCore.QCoreApplication.translate
            self.pushButton_2.setText(_translate("MainWindow", "중지"))
            mandle_run.start_run(self)
        else:
            self.excute_form = 0
            print('stop')
            _translate = QtCore.QCoreApplication.translate
            self.pushButton_2.setText(_translate("MainWindow", "실행"))
            mandle_run.exit_pro(self)
    #종료버튼
    def exit_pro(self):
        sys.exit()
        

        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
