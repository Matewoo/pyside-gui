from PySide6.QtCore import Qt 
from PySide6.QtGui import QKeySequence, QPixmap, QCloseEvent, QImage 
from PySide6.QtGui import QPainter, QColor, QIcon
from PySide6.QtWidgets import QApplication, QMenuBar, QToolBar 
from PySide6.QtWidgets import QWidget, QFileDialog, QFrame
from PySide6.QtWidgets import QMainWindow, QMessageBox, QVBoxLayout, QPushButton
import sys

# Our own widget type (for later) 
class MyPaintArea(QWidget): 
    def __init__(self, parent: QWidget): 
        super().__init__(parent) 
        self.setMinimumWidth(640) # Größe des neuen Widgets muss man  
        self.setMinimumHeight(480) # unbedingt selbst einstellen! 
        self.image: QImage = QImage(640, 480, QImage.Format_RGB32) # 640x480pix 
        self.image.fill(QColor(255, 255, 255)) # mit weiß löschen 
        # ... man braucht sicher noch mehr ;-) ... 
 
    # Diese Methode wird immer aufgerufen, wenn das GUI-Element auf dem Bild- 
    # schirm dargestellt warden soll. Man programmiert hier, wie es sich 
    # "selbst zeichnen" soll. Einfach mal ausprobieren! 
    def paintEvent(self, event): 
        painter: QPainter = QPainter(self) 
        # hier kann man nun auf das Widget zeichnen 
        # Sinnvoll ist z.B.  
        # painter.drawImage(<x-Koord: int>., <y-Koord: int>., <ein QImage>) 
        # oder zum Testen painter.fillRect(…), drawLine(…) o.ä. 
        # (siehe Doku der Klasse QPainter in PySide6) 
 
    # Diese Methode wird jedes Mal aufgerufen, wenn die Maus über unserem 
    # GUI-Element gedrückt wird 
    def mousePressEvent(self, event): 
        # Mit einer solchen Abfrage kann man überprüfen, welcher Knopf es war 
        if event.button() == Qt.MouseButtons.LeftButton: 
            print("Left mouse button pressed")
            # ... 
 
    # Hier das gleiche für das Loslassen von Maustasten 
    def mouseReleaseEvent(self, event):
        print("Mouse released")
    # ... 
    # Und diese Methode wird aufgerufen, falls die Maus über unserem 
    # GUI-Element bewegt wird. Achtung: Man muss natürlich prüfen, ob die 
    # Taste gedrückt wurde... 
    def mouseMoveEvent(self, event):
        print("Mouse moved")
 
 
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




    def __init__(self, parent: QWidget): 
        # call parent constructor (required for QMainWindow) 
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

        self.info_action.triggered.connect(self.show_info)

        self.quit_action.triggered.connect(self.show_quit_warning)



        self.nice_toolbar: QToolBar = self.addToolBar("Some Nice Tools")
        self.nice_toolbar.addAction("Open")
        self.nice_toolbar.addAction("Save")
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
