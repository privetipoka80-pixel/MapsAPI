import os
import sys

import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt6.QtCore import Qt
from themes import dark_style, light_style

SCREEN_SIZE = [800, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.x = 37.530887
        self.y = 55.703118
        self.scale = [0.002, 0.002]
        self.theme_api = "dark"
        self.getImage()
        self.initUI()

    def getImage(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        self.scale_resp = ','.join(map(str, self.scale))
        self.l1 = self.x
        self.l2 = self.y

        ll_spn = f'll={round(self.l1, 6)},{round(self.l2, 6)}&spn={(self.scale_resp)}'

        map_request = f"{server_address}{ll_spn}&apikey={api_key}&theme={self.theme_api}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code,
                  "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

        self.theme_button = QPushButton(self)
        self.theme_button.setText('Светлая тема')
        self.theme_button.resize(140, 40)
        self.theme_button.move(650, 0)
        self.theme_button.clicked.connect(self.theme)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        sc = 2
        if event.key() == Qt.Key.Key_Up:
            print('вверх')
            self.y += 0.002
            self.getImage()
            self.newImage()
            print(self.y)

        elif event.key() == Qt.Key.Key_Right:
            print('вправо')
            self.x += 0.002
            self.getImage()
            self.newImage()
            print(self.x)
        elif event.key() == Qt.Key.Key_Left:
            print('влево')
            self.x -= 0.002
            self.getImage()
            self.newImage()
            print(self.x)
        elif event.key() == Qt.Key.Key_Down:
            print('вниз')
            self.y -= 0.002
            self.getImage()
            self.newImage()
            print(self.y)

        elif event.key() == Qt.Key.Key_PageUp:
            self.scale[0] *= sc
            self.scale[1] *= sc
            if self.scale[0] < 90:
                self.getImage()
                self.newImage()

        elif event.key() == Qt.Key.Key_PageDown:
            self.scale[0] /= sc
            self.scale[1] /= sc
            if 0 < self.scale[0]:
                self.getImage()
                self.newImage()

    def newImage(self):
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def theme(self):
        theme = self.sender().text()
        if theme == 'Светлая тема':
            self.theme_api = 'light'
            self.getImage()
            self.newImage()
            self.theme_button.setText('Тёмная тема')
            self.setStyleSheet(light_style)
        else:
            self.theme_api = 'dark'
            self.getImage()
            self.newImage()
            self.theme_button.setText('Светлая тема')
            self.setStyleSheet(dark_style)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
