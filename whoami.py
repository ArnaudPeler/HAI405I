from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout, QPushButton, QGridLayout, QLabel
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt
import os, json

class SelectGridWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Veuillez séléctioner une grille')
        self.grids_list = self.detect_grid_folders()

        self.selector = QComboBox()
        for grid in self.grids_list:
                self.selector.addItem(grid.split('/')[1])
        button = QPushButton('Séléctioner')
        button.clicked.connect(self.button_clicked,self.selector.currentIndex())

        layout = QVBoxLayout()
        layout.addWidget(self.selector)
        layout.addWidget(button)
        self.setLayout(layout)

        self.show()

    def detect_grid_folders(self):
        grids_list = []

        if not os.path.isdir('grids'):
            raise Exception('"grids" folder not found')
        else:
            if not os.listdir('grids'):
                raise Exception('"grids" folder is empty')
            else:
                for dir in os.listdir('grids'):
                    if os.path.isdir('grids/'+dir) and os.path.isfile('grids/'+dir+'/'+dir+'.json'): # On va considérer que les dossier de grille sont bien structurés (fichier .json à l'intérieur + toutes les images en .png)
                        grids_list.append('grids/'+dir)
                if len(grids_list) == 0:
                    raise Exception('no grid folder in "grids" folder')
        return grids_list

    def button_clicked(self, index):
        self.w = GameWindow(self.grids_list[index])
        self.close()

class GameWindow(QWidget):
    def __init__(self, grid_path):
        super().__init__()
        self.grid_path = grid_path
        with open(grid_path+'/'+grid_path.split('/')[1]+'.json', "r") as datas:
            self.grid_datas = json.load(datas)

        self.grid_layout = self.grid_datas.pop('layout')

        self.item_list = []

        self.setWindowTitle(grid_path.split('/')[1])

        self.show()
        self.make_game_layout()

    def make_game_layout(self):
        layout = QGridLayout()
        k = 0
        for i in range(self.grid_layout[0]):
            for j in range(self.grid_layout[1]):
                game_item = GameItem(self.grid_path, self.grid_datas[list(self.grid_datas)[k]])
                self.item_list.append(game_item)

                layout.addWidget(game_item, i, j)

                k+=1

        self.setLayout(layout)

class GameItem(QLabel):
    def __init__(self, dir, datas):
        super().__init__()
        self.name = datas['nom']
        self.image_path = dir + '/' + self.name + '.png'
        self.datas = datas

        self.image = QPixmap(self.image_path)
        self.setPixmap(self.image)

        self.image_clicked = QPixmap(self.image_path)
        qp = QPainter(self.image_clicked)
        qp.setPen(QPen(Qt.red, 3))
        qp.drawLine(0, 0, 100, 100)
        qp.end()


        self.is_clicked = False

        self.mousePressEvent = self.when_clicked

    def when_clicked(self, event):
        if self.is_clicked == False:
            self.setPixmap(self.image_clicked)
            self.is_clicked = True
        else:
            self.setPixmap(self.image)
            self.is_clicked = False

whoami = QApplication.instance() # Utile pour travailler aec l'IDE
if not whoami:
    whoami = QApplication([])

    select_grid_window = SelectGridWindow()

whoami.exec_()