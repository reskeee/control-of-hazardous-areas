from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import uic
import sys
from main1 import predict
from colorama import Back


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/main.ui", self)

        self.startButton.clicked.connect(self.start_prediction)
        self.changeButton.clicked.connect(self.choose_video)
        self.zoneButton.clicked.connect(self.choose_zones)

        self.video_filename = None
        self.zones_filename = None

    def start_prediction(self):
        print(Back.GREEN + "start_click")
        print(Back.GREEN + str(self.video_filename))
        print(Back.GREEN + str(self.zones_filename))
        if self.video_filename and self.zones_filename:
            predict(self.video_filename, self.zones_filename)
        else:
            if not self.video_filename:
                self.label_2.setStyleSheet('background-color: red;')
            if not self.video_filename:
                self.label.setStyleSheet('background-color: red;')

    def choose_video(self):
        print("change_file")
        file = QFileDialog.getOpenFileName(
            self, "Выберите видео для обработки", '', "*.mp4;;*.avi")[0]
        self.label.setText(file)
        self.video_filename = file
        self.label.setStyleSheet('background-color: white;')

    def choose_zones(self):
        print("zones")
        file = QFileDialog.getOpenFileName(
            self, "Выберите описания зон", '', "*.txt")[0]
        self.label_2.setText(file)
        self.zones_filename = file
        self.label_2.setStyleSheet('background-color: white;')

# def except_hook(cls, exception, traceback):
#     sys.excepthook(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    main_window = MainWindow()
    main_window.show()
    # sys.excepthook = except_hook
    sys.exit(app.exec())
