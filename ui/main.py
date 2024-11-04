import sys
import re
import time
import logging
import pyautogui
import pydirectinput
from src import songSheet, play_song, Song
from typing import Optional as Opt
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QApplication, QMainWindow, \
    QLabel, QSpacerItem, QSizePolicy as QSize, QSlider, QTextEdit
from PyQt5.QtGui import QResizeEvent, QMouseEvent

logging.basicConfig()
LOGGER = logging.getLogger("genshin-music-app")


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    LOGGER.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception


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
        self.delay_layout = QVBoxLayout()
        self.song_config_layout = QVBoxLayout()
        self.infolabel_layout = QVBoxLayout()

        # * Define Widget variables
        self.song_picker: Opt[QComboBox] = None
        self.custom_label: Opt[QLabel] = None
        self.custom_input: Opt[QTextEdit] = None
        self.play_button: Opt[QPushButton] = None
        self.info_label: Opt[QLabel] = None
        self.delay_slider: Opt[QSlider] = None
        self.delay_label: Opt[QLabel] = None

        # * Song Picker
        self.init_songpicker()
        # * Button
        self.init_play_button()
        # * Delay Slider
        self.init_delay_slider()
        # * Info Label
        self.init_info_label()

        # * Spacer
        spacer = QSpacerItem(20, 40, QSize.Minimum, QSize.Expanding)

        # * Layout Config
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        # self.songpicker_layout.setContentsMargins(50, 0, 50, 0)
        self.song_config_layout.setContentsMargins(50, 0, 50, 0)
        self.delay_layout.setContentsMargins(0, 20, 0, 70)
        self.infolabel_layout.setContentsMargins(50, 0, 50, 0)

        # * Add Widgets to Layouts
        self.layout.addWidget(MyBar(parent=self, title="Genshin Music App"))
        self.layout.addLayout(self.main_layout)
        self.main_layout.addLayout(self.song_config_layout)
        self.song_config_layout.addLayout(self.songpicker_layout)
        self.song_config_layout.addLayout(self.delay_layout)
        # self.song_config_layout.addWidget(self.delay_slider)
        self.main_layout.addLayout(self.infolabel_layout)
        self.main_layout.addItem(spacer)

        # * Window Settings
        self.setMinimumSize(800, 600)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Genshin Music App")
        self.setCentralWidget(widget)
        widget.setLayout(self.layout)

    def init_songpicker(self):
        """Initialize the song picker dropdown."""

        self.song_picker = QComboBox(self)
        for song in songSheet:
            self.song_picker.addItem(song)
        self.song_picker.addItem("Custom")
        self.song_picker.currentIndexChanged.connect(self.songpicker_changed)
        self.songpicker_layout.addWidget(self.song_picker)
        self.song_picker.setCursor(Qt.PointingHandCursor)
        self.song_picker.setStyleSheet("""
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
                """)

    def songpicker_changed(self):
        if self.song_picker.currentText() == "Custom":
            self.custom_label = QLabel(
                "Enter scripts from <a href=\"https://www.reddit.com/r/genshinmusicapp/\">r/genshinmusicapp</a>")
            self.custom_label.setOpenExternalLinks(True)
            self.custom_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
            self.custom_label.setStyleSheet("font-size: 20px;")
            self.custom_input = QTextEdit()
            self.custom_input.setStyleSheet(
                """
                    QTextEdit {
                        border: 1px solid gray; border-radius: 9px; font-size: 20px;
                    }
                """
            )
            self.song_config_layout.addWidget(self.custom_label)
            self.song_config_layout.addWidget(self.custom_input)
            return
        self.song_config_layout.removeWidget(self.custom_label)
        self.song_config_layout.removeWidget(self.custom_input)
        self.custom_label.deleteLater()
        self.custom_input.deleteLater()

    def init_info_label(self):
        self.info_label = QLabel("")
        self.info_label.setWordWrap(True)
        self.infolabel_layout.addWidget(self.info_label)

    def init_play_button(self):
        self.play_button = QPushButton("Play Song")
        self.play_button.clicked.connect(self.play_button_clicked)
        self.songpicker_layout.addWidget(self.play_button)
        self.play_button.setCursor(Qt.PointingHandCursor)
        self.play_button.setStyleSheet("""
                QPushButton {
                    border: 1px solid gray; border-radius: 9px; padding: 15px 5px; font-size: 20px;
                }

                QPushButton:hover { background-color: #303030;  }
            """)

    def _show_delay(self, delay: int, fmt_str: str = "Starting in {n}s...",
                    final_msg: str = "To stop the song, move your mouse to the top left corner of your screen"):
        for i in range(delay, 0, -1):
            self.info_label.setText(fmt_str.format(n=i))
            QApplication.processEvents()
            time.sleep(1)
        self.info_label.setText(final_msg)
        # ! Don't know why, but this is needed to update the label
        for _ in range(10):
            QApplication.processEvents()

    def play_button_clicked(self):
        is_custom = False
        if self.song_picker.currentText() == "Custom":
            is_custom = True
            song = self.custom_input.toPlainText()
            m = re.match("""((?P<name>.*?) BPM:(?P<BPM>\d+) \|\| )?(?P<notes>.+)""", song, re.DOTALL)
            song = Song(name=m.group("name"), bpm=int(m.group("BPM")), notes=m.group("notes"))
        else:
            song = songSheet[self.song_picker.currentText()]
        self.play_button.setDisabled(True)
        color = "#FF3030"
        try:
            self.info_label.setStyleSheet("font-size: 30px; color: white;")
            self.info_label.setAlignment(Qt.AlignLeft)
            self._show_delay(
                delay=self.delay_slider.value(), fmt_str="Starting in {n}s...",
                final_msg=f"Now Playing:\t{song.name}\nTo stop the song, move your mouse to the top left corner of your screen\n"
            )
            play_song(song, is_custom)
            self.info_label.setText(f"Song Finished!!")
            color = "#00FFFF"
        except pydirectinput.FailSafeException:
            self.info_label.setText(f"Song Stopped by mouse movement.")
            color = "#FF3030"
        finally:
            self.info_label.setStyleSheet(f"font-size: 40px; color: {color};")
            self.info_label.setAlignment(Qt.AlignCenter)
            self.play_button.setDisabled(False)

    def init_delay_slider(self):
        self.delay_slider = QSlider(Qt.Horizontal)
        self.delay_slider.setRange(0, 10)
        self.delay_slider.setValue(2)
        self.delay_slider.setTickInterval(1)
        self.delay_slider.setTickPosition(QSlider.TicksBelow)
        self.delay_slider.setSingleStep(1)

        # Label for the slider
        self.delay_label = QLabel("Delay: 2s")
        self.delay_label.setStyleSheet("font-size: 20px; color: white;")
        self.delay_layout.addWidget(self.delay_label)
        self.delay_slider.valueChanged.connect(lambda: self.delay_label.setText(f"Delay: {self.delay_slider.value()}s"))
        # Styling the slider
        self.delay_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: #181818;
                margin: 2px 0;
            }
            QSlider::handle:horizontal {
                background: #77e;
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -2px 0;
                border-radius: 3px;
            }
            QSlider::handle:horizontal:hover {
                background: #99f;
                border: 1px solid #5c5c5c;
                border-radius: 3px;
                width: 18px;
                margin: -2px 0;
            }
        """)
        self.delay_slider.setCursor(Qt.PointingHandCursor)
        self.delay_layout.addWidget(self.delay_slider)


class MyBar(QWidget):
    def __init__(self, parent, title: str = "", btn_size: int = 35, *args, **kwargs):
        super(MyBar, self).__init__()
        self.parent = parent
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.title = QLabel(title)

        btn_size = 35

        self.btn_close = QPushButton("✕")
        self.btn_close.clicked.connect(self.parent.close)
        self.btn_close.setFixedSize(btn_size, btn_size)
        self.btn_close.setStyleSheet("""
            QPushButton { background-color: #000000FF; color: white; }
            QPushButton:hover { background-color: #ff0000; }
            """)

        self.btn_max = QPushButton("ロ")
        self.btn_max.clicked.connect(self.btn_max_clicked)
        self.btn_max.setFixedSize(btn_size, btn_size)
        self.btn_max.setStyleSheet("""
        QPushButton { background-color: #000000FF; color: white; }
        QPushButton:hover { background-color: #303030; }""")
        self.isMaximized = False

        self.btn_min = QPushButton("―")
        self.btn_min.clicked.connect(self.parent.showMinimized)
        self.btn_min.setFixedSize(btn_size, btn_size)
        self.btn_min.setStyleSheet("""
        QPushButton { background-color: #000000FF; color: white; }
        QPushButton:hover { background-color: #303030; }""")

        self.title.setFixedHeight(btn_size)
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.btn_max)
        self.layout.addWidget(self.btn_close)

        self.title.setStyleSheet("background-color: #191919; color: white;")
        self.setLayout(self.layout)
        self.setStyleSheet("background-color: #000; color: white;")
        self.start = QPoint(0, 0)
        self.end = self.start
        self.movement = self.end - self.start
        self.pressing = False
        self.setMaximumHeight(btn_size)

    def resizeEvent(self, event: QResizeEvent):
        super(MyBar, self).resizeEvent(event)
        self.title.setFixedWidth(self.parent.width())

    def mousePressEvent(self, event: QMouseEvent):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                    self.mapToGlobal(self.movement).y(),
                                    self.parent.width(),
                                    self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.pressing = False

    def btn_max_clicked(self):
        (self.parent.showNormal if self.isMaximized else self.parent.showMaximized)()
        self.isMaximized = not self.isMaximized


def run_app():
    app = QApplication([])
    window = Main()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_app()
