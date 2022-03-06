# README

## Clonning & Launch

Vous pouvez cloner directement le projet avec :

```bash
$ git clone https://github.com/ArnaudPeler/HAI405I.git
```

La version de Python utilisé est Python 3.10 et les seules librairies non fournies directement avec Python viennent de `PyQt5` installables avec :

``` bash
$ pip install pyqt5
```

à supposer que vous avez déjà `pip` d'installé.

Il ne vous reste plus qu'à lancer `whoami.py` situé à la racine du projet avec la commande

```bash
$ python3 whoami.py
```



## Comment jouer

Au lancement du programme, vous tomberez sur une fenêtre vous laissant choisir une des grilles disponible. Il y en à 2 pour le moment, une basé sur les exemples d'images données pour le projet, et une version miniature de celle ci.

Au début du jeu, l'ordinateur choisit un personnage au hasard parmi ceux présent sur la grille et vous devez trouver lequel en posant des questions grâce aux boîtes de sélection en bas de la fenêtre.

Cliquer sur un portrait vous permet de le barrer en rouge et ainsi indiquer ce n'est pas le personnage que vous cherchez.

Le jeux se ferme automatiquement quand vous trouvez le nom du personnage choisi par l'ordinateur.