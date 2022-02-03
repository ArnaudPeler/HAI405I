"""from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMainWindow
import os

class MenuWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Menu')

        play_button = QPushButton('Jouer !')
        play_button.clicked.connect(self._play)

        edit_button = QPushButton('Editer une grille !')

        menu_widow_layout = QVBoxLayout()
        menu_widow_layout.addWidget(play_button)
        menu_widow_layout.addWidget(edit_button)
        self.setLayout(menu_widow_layout)
        self.show()


    def _play(self):
        self.w = SelectGridWindow()
        self.close()

class SelectGridWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Veuillez séléctioner une grille')
        self.show()

whoami = QApplication.instance()
if not whoami:
    whoami = QApplication([])

menu_window = MenuWindow()

whoami.exec_()"""

for i in range(4):
    for j in range(4):
        print(i,j)