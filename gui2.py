from PySide6.QtCore import Qt 
from PySide6.QtGui import QKeySequence, QPixmap, QCloseEvent, QImage 
from PySide6.QtGui import QPainter, QColor, QIcon
from PySide6.QtWidgets import QApplication, QMenuBar, QToolBar 
from PySide6.QtWidgets import QWidget, QFileDialog, QFrame
from PySide6.QtWidgets import QMainWindow, QMessageBox, QVBoxLayout, QPushButton
import sys

class MyPaintArea(QWidget): 
    def __init__(self, parent: QWidget): 
        super().__init__(parent)

        self.setMinimumWidth(640)
        self.setMinimumHeight(480)
        self.image: QImage = QImage(640, 480, QImage.Format_RGB32)
        self.image.fill(QColor(255, 255, 255))
        self.drawing = False

    def load_image(self, filename):
        self.image = QImage(filename)
        self.update()

    def paintEvent(self, event):
        painter: QPainter = QPainter(self)
        painter.drawImage(0, 0, self.image)

    def mousePressEvent(self, event):
        painter = QPainter(self.image)
        if event.button() == Qt.MouseButtons.LeftButton: 
            self.drawing = True
            self.lastPoint = event.pos()
            painter.drawPoint(event.pos())
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButtons.LeftButton:
            self.drawing = False

    def mouseMoveEvent(self, event):
        if (event.buttons() and Qt.MouseButtons.LeftButton) and self.drawing:
            painter = QPainter(self.image)
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()
# Our own Main Window type 
class MyWindow(QMainWindow): 

    def say_hello(self):
        print("Hello World!")

    def show_quit_warning(self):
        # open a simple dialog window to say hello
        ret = QMessageBox.question(self, "ALARM!", "Möchtest Du das Programm wirklich schließen? :(", QMessageBox.Yes, QMessageBox.No)
        if ret == QMessageBox.Yes:
            self.close()
        else:
            print("Programm wird fortgesetzt")
    
    def show_info(self):
        QMessageBox.information(self, "Info", "This is a simple text editor.", QMessageBox.Ok)

    def load_file(self):
        file_name, selected_filter = QFileDialog.getOpenFileName(self, "Open Image", "", "PNG Files (*.png)")
        if file_name:  # make sure a file name was selected
            self.paint_area.load_image(file_name)

    def save_file(self):
        file_name, selected_filter = QFileDialog.getSaveFileName(self, "Save As", "picture", "PNG Files (*.png)") 
        if file_name:  # make sure a file name was selected
            self.paint_area.image.save(file_name) 

    def __init__(self, parent: QWidget): 

        super().__init__(parent) 

        self.paint_area: MyPaintArea = MyPaintArea(self)
        layout = QVBoxLayout()
        layout.addWidget(self.paint_area)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)

        self.setCentralWidget(centralWidget)

 
        # Die drei Punkte am Ende benutzt man, falls noch weitere Dialoge folgen 
        # (das ist nur eine ästhetische Konvention; Qt ist das egal). 
        self.file_menu: QMenuBar = self.menuBar().addMenu("File...")
        self.help_menu: QMenuBar = self.menuBar().addMenu("Help...")
        #Nun kann man Untermenüs als „Aktionen“ (QAction) hinzufügen2: 
        self.open_action = self.file_menu.addAction("Open File") 
        self.open_action.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_O))

        self.saveAs_action = self.file_menu.addAction("Save As...") 
        self.saveAs_action.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_S)) 

        self.quit_action = self.file_menu.addAction("Quit") 
        self.quit_action.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_Q)) 
        #self.fancy_action.setIcon(QPixmap("dateiname_für_icon.png"))
        self.info_action = self.help_menu.addAction("Info") 
        self.info_action.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_I)) 

        self.open_action.triggered.connect(self.load_file)
        self.saveAs_action.triggered.connect(self.save_file)
        self.info_action.triggered.connect(self.show_info)

        self.quit_action.triggered.connect(self.show_quit_warning)



        self.nice_toolbar: QToolBar = self.addToolBar("Some Nice Tools")
        self.nice_toolbar.addAction("Open", self.load_file)
        self.nice_toolbar.addAction("Save", self.save_file)
        self.nice_toolbar.addAction("Info", self.show_info)
        self.nice_toolbar.addAction("Quit", self.show_quit_warning)


 
# our main program starts here, Python-style 
if __name__ == "__main__": 
    # create an application object (needs cmd-line arguments) 
    app: QApplication = QApplication(sys.argv) 
 
    # Create the main window. 
    main_window: MyWindow = MyWindow(None)
    #main_window.resize(800, 600)
    main_window.setWindowTitle("Joa")
    main_window.show() 
 
    # Start the event loop. 
    # Ends only after closing the main window 
    app.exec()
