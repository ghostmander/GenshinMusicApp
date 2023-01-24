from src.songs import songSheet
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QApplication, QMainWindow, QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QResizeEvent, QMouseEvent


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        # * Main Widget
        widget = QWidget()
        widget.setStyleSheet("background-color: #222; color: white;")

        # * Layouts
        self.layout = QVBoxLayout()
        self.main_layout = QVBoxLayout()
        self.songpicker_layout = QHBoxLayout()

        # * Song Picker
        self.songPicker = QComboBox(self)
        for song in songSheet:
            self.songPicker.addItem(song)
        self.songpicker_layout.addWidget(self.songPicker)
        self.songPicker.setStyleSheet(
            """
                QComboBox {
                    border: 1px solid gray; border-radius: 9px; padding: 15px 5px; font-size: 20px;
                }

                QComboBox:!editable, QComboBox::drop-down:editable {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                stop: 0 #181818, stop: 0.4 #222222,
                                                stop: 0.5 #232323, stop: 1.0 #282828);
                }

                QComboBox:!editable:on, QComboBox::drop-down:editable:on {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                stop: 0 #282828, stop: 0.4 #232323,
                                                stop: 0.5 #222222, stop: 1.0 #181818);
                    border-bottom-right-radius: 0px;
                    border-bottom-left-radius: 0px;
                }

                QComboBox::drop-down {
                    subcontrol-origin: padding;
                    subcontrol-position: top right;
                    width: 30px;
                    border-left-width: 1px;
                    border-left-color: #181818;
                    border-left-style: solid;
                    border-top-right-radius: 9px;
                    border-bottom-right-radius: 9px;
                }
                
                QComboBox::down-arrow { image: url(ui/assets/dropdown.png); }
                
                QComboBox QAbstractItemView {
                    border: 1px solid darkgray;
                    outline: 0;
                    selection-background-color: black;
                }
                """
        )

        # * Button
        # TODO: Make this button actually do something
        self.button = QPushButton("Select Song")
        self.button.clicked.connect(self.the_button_was_clicked)
        self.songpicker_layout.addWidget(self.button)

        # * Spacer
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum,
                             QSizePolicy.Expanding)

        # * Layout Config
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.songpicker_layout.setContentsMargins(50, 0, 50, 0)

        # * Add Widgets to Layouts
        self.layout.addWidget(MyBar(self))
        self.layout.addLayout(self.main_layout)
        self.main_layout.addLayout(self.songpicker_layout)
        self.main_layout.addItem(spacer)

        # * Window Settings
        self.setMinimumSize(800, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Genshin Music App")
        self.setCentralWidget(widget)
        widget.setLayout(self.layout)

    def the_button_was_clicked(self):
        print(self.songPicker.currentText())


class MyBar(QWidget):
    def __init__(self, parent):
        super(MyBar, self).__init__()
        self.parent = parent
        print(self.parent.width())
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.title = QLabel("Genshin Music App")

        btn_size = 35

        self.btn_close = QPushButton("✕")
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.setFixedSize(btn_size, btn_size)
        self.btn_close.setStyleSheet(
            """QPushButton { background-color: #000000FF; color: white; }"""
            """QPushButton:hover { background-color: #ff0000; }"""
        )

        self.btn_min = QPushButton("―")
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.setFixedSize(btn_size, btn_size)
        self.btn_min.setStyleSheet(
            """QPushButton { background-color: #000000FF; color: white; }"""
            """QPushButton:hover { background-color: #303030; }"""
        )

        self.title.setFixedHeight(35)
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.btn_close)

        self.title.setStyleSheet("background-color: #191919; color: white;")
        self.setLayout(self.layout)
        self.setStyleSheet("background-color: #000; color: white;")
        self.start = QPoint(0, 0)
        self.pressing = False
        self.setMaximumHeight(btn_size)

    def resizeEvent(self, QResizeEvent):
        super(MyBar, self).resizeEvent(QResizeEvent)
        self.title.setFixedWidth(self.parent.width())

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                    self.mapToGlobal(self.movement).y(),
                                    self.parent.width(),
                                    self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False

    def btn_close_clicked(self):
        self.parent.close()

    def btn_min_clicked(self):
        self.parent.showMinimized()


app = QApplication([])
window = Main()
window.show()
app.exec_()
