import random
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout, QPushButton, QGridLayout, QLabel, QHBoxLayout, QMessageBox
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
        button.clicked.connect(self.button_clicked)

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

    def button_clicked(self):
        self.w = GameWindow(self.grids_list[self.selector.currentIndex()])
        self.close()

class GameWindow(QWidget):
    def __init__(self, grid_path):
        super().__init__()
        self.grid_path = grid_path
        with open(grid_path+'/'+grid_path.split('/')[1]+'.json', "r") as datas:
            self.grid_datas = json.load(datas)

        self.grid_layout = self.grid_datas.pop('layout')

        self.item_list = []
        self.questions_n_answers = {}

        self.setWindowTitle(grid_path.split('/')[1])

        self.layout = QVBoxLayout()
        self.items_layout()
        self.questions_layout()
        self.setLayout(self.layout)

        self.random_pick = random.choice(self.item_list)

        self.show()

    def items_layout(self):
        layout = QGridLayout()
        k = 0
        for i in range(self.grid_layout[0]):
            for j in range(self.grid_layout[1]):
                game_item = GameItem(self.grid_path, self.grid_datas[list(self.grid_datas)[k]])
                self.item_list.append(game_item)

                layout.addWidget(game_item, i, j)

                k+=1

        self.layout.addLayout(layout)

    def questions_layout(self): #besoin de changer la disposition des éléments pour éviter que les sélections soient coupés
        layout = QHBoxLayout()

        layout.addWidget(QLabel("Question :"))
        for item in self.item_list:
            for question in list(item.datas.keys()):
                if question not in self.questions_n_answers:
                    self.questions_n_answers[question] = item.datas[question]
                else:
                    for answer in item.datas[question]:
                        if answer not in self.questions_n_answers[question]:
                            self.questions_n_answers[question].append(answer)

        self.question_selector = QComboBox()
        self.question_selector.addItems(list(self.questions_n_answers.keys()))
        self.question_selector.currentTextChanged.connect(self.change_answer_selection)
        layout.addWidget(self.question_selector)

        self.answer_selector = QComboBox()
        self.change_answer_selection(self.question_selector.currentText())
        layout.addWidget(self.answer_selector)

        submit_button = QPushButton('Submit')
        submit_button.clicked.connect(self.submit_button_cliked)
        layout.addWidget(submit_button)

        self.layout.addLayout(layout)

    def change_answer_selection(self, text):
        self.answer_selector.clear()
        self.answer_selector.addItems(self.questions_n_answers[text] + ['aucun'])

    def submit_button_cliked(self):

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Answer !")
        if self.answer_selector.currentText() in self.random_pick.datas[self.question_selector.currentText()]\
                or (self.answer_selector.currentText() == 'aucun' and self.random_pick.datas[self.question_selector.currentText()]==[]):
            dlg.setText("C'est vrai !")
        else:
            dlg.setText("C'est faux !")
        button = dlg.exec()

        if button == QMessageBox.Ok: #erreur à la fermeture de la boite de dialogue
            if self.random_pick.name == self.answer_selector.currentText():
                dlg.setWindowTitle("Bravo !")
                dlg.setText("Vous avez trouvé !")
                button = dlg.exec()
                if button == QMessageBox.Ok:
                    self.close()


class GameItem(QLabel):
    def __init__(self, dir, datas):
        super().__init__()
        self.name = datas['nom'][0]
        self.image_path = dir + '/' + self.name + '.png'
        self.datas = datas

        self.image = QPixmap(self.image_path)
        self.setPixmap(self.image)

        self.image_crossed = QPixmap(self.image_path)
        qp = QPainter(self.image_crossed)
        qp.setPen(QPen(Qt.red, 3))
        qp.drawLine(0, 0, 100, 100) # à changer pour mieux correspondre à la taille de l'image
        qp.end()


        self.is_crossed = False

        self.mousePressEvent = self.when_crossed

    def when_crossed(self, event):
        if self.is_crossed == False:
            self.setPixmap(self.image_crossed)
            self.is_crossed = True
        else:
            self.setPixmap(self.image)
            self.is_crossed = False

whoami = QApplication.instance() # Utile pour travailler aec l'IDE
if not whoami:
    whoami = QApplication([])

    select_grid_window = SelectGridWindow()

whoami.exec_()