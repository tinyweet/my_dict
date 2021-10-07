import json

from PyQt5.QtCore import QRect, QTimer, Qt, QSize
from PyQt5.QtGui import QCursor, QFont
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QApplication, QWidget

from src.UI.result import ResultWindow
from src.youdao import YouDaoFanYi


class TipWindow(QWidget):
    last_text = ""

    def __init__(self, youdao: YouDaoFanYi):
        super().__init__()
        self.setMinimumSize(QSize(360, 280))
        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.on_data_changed)
        self.youdao = youdao
        # self.setAttribute(Qt.WA_TranslucentBackground)            # 窗体背景透明
        # 窗口置顶，无边框，在任务栏不显示图标
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.BypassWindowManagerHint | Qt.FramelessWindowHint | Qt.Tool)
        self.label_src = QLabel()
        font = QFont()
        font.setFamily("Mono")
        font.setPointSize(16)
        font.setWeight(75)
        font.setBold(True)
        self.label_src.setFont(font)
        self.result = ResultWindow(self)
        vbox = QVBoxLayout()
        vbox.addWidget(self.label_src)
        vbox.addWidget(self.result)
        self.setLayout(vbox)
        self.timer_hide = QTimer()
        self.timer_hide.timeout.connect(self.on_auto_hide)

    @staticmethod
    def on_play(media_player: QMediaPlayer):
        try:
            media_player.stop()
            media_player.play()
        except Exception as ex:
            print("Exception", ex)

    def on_data_changed(self):
        data = self.clipboard.text()
        if self.last_text != data:
            self.last_text = data
            return
        self.last_text = ""
        is_word, result = self.youdao.translate(data)
        print(json.dumps(result, indent=4, ensure_ascii=False))
        if is_word:
            succeed = self.result.show_word_result(result)
            self.label_src.setText(data)
            self.label_src.show()
        else:
            succeed = self.result.show_text_result(result)
            self.label_src.hide()
        if succeed:
            self.show()

    def on_auto_hide(self):
        pos = QCursor.pos()
        geometry = self.geometry()
        geometry: QRect
        geometry.adjust(-5, -5, 5, 5)
        if geometry.contains(pos):
            self.timer_hide.start(1000)
            return
        self.timer_hide.stop()
        self.hide()

    def show(self):
        self.move(QCursor.pos())
        self.timer_hide.start(3000)
        super().show()
