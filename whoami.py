from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout, QPushButton
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
        self.setWindowTitle(grid_path.split('/')[1])

        print(self.grid_datas)

        self.show()

    def make_layout(self):
        pass



whoami = QApplication.instance() # Utile pour travailler aec l'IDE
if not whoami:
    whoami = QApplication([])

    select_grid_window = SelectGridWindow()

whoami.exec_()