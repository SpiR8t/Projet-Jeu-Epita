# Projet-Jeu-Epita
Projet de groupe sur la création d'un jeux sur python

# Installation du jeu
Pour installer le jeu ou y contribuer, il est nécessaire de passer par différentes étapes. À terme, toutes ces étapes devraient être faite plus ou moins automatiquement.

### 1. Cloner/télécharger le répo
Pour obtenir les différents fichiers du jeu, il faut soit cloner le repo avec une clé SSH ou via HTTP en faisant :
- via HTTP :
```
git clone https://github.com/SpiR8t/Projet-Jeu-Epita.git
```
- via SSH :
```
git clone git@github.com:SpiR8t/Projet-Jeu-Epita.git
```
Il est également possible de télécharger le projet compréssé dans une archive ZIP et ensuite de le décompresser.

### 2. Créer un environnement python
Il faut créer un environnement python spécifique au projet ou seront installé les librairies nécessaires. 
Pour cela, en se trouvant à la racine du répertoire du projet, entrer la commade suivante (il est possible de mettre le nom que l'on souhaite à la place de ```projet_prog_s1```) :
```
python -m venv projet_prog_s1
```
Puis on doit activer l'environnement en faisant :
```
projet_prog_s1\Scripts\activate
```

On peut maintenant installer les librairies nécessaires au projet.

### 3. Installer les librairies nécéssaires
Voici les différentes librairies que notre code utilise, leur utilité, et comment les installer :
- aiortc : utilisée pour faire la connection P2P. Installation :
```pip install aiortc```

- requests : utilisée pour communiquer avec la base de donnée firebase. Installation :
```pip install requests```

- pygame : utilisée pour implémenter tout le fonctionnemment du jeu. Installation :
```pip install pygame```

- PIL ou Pillow : utilisée pour importer et charger l'image qui permet de générer la map du jeu. Installation :
```pip install Pillow```

# Couleurs de pixels utilisés pour la map
Les tests sont fait dans l'ordre des lignes du tableau donc on applique la valeur dans une ligne que si on entre paqs dans une ligne plus haut.
| R | G | B | Description | Numéro de tuile dans la matrice |
| --- | --- | --- | --- | --- |
| `106` | `190` | `48` | Place un mur | 1 2 2 |
| `187` | `135` | `b` | Place un levier par défaut désactivé, appartenant au group `b` | 1 0 10 |
| `122` | `40 <= g <= 47` | `b` | Place une porte appartenant au groupe `b`, par défaut fermée, avec `g` définissant l’orientation d’ouverture et de fermeture en suivant cette logique :   40 = NE (ouverture NW), 41 = SW (ouverture NW), 42 = NW (ouverture NE), 43 = SE (ouverture NE)   44 = NE (ouverture SE), 45 = SW (ouverture SE), 46 = NW (ouverture SW), 47 = SE (ouverture SW).   Les tuiles entre 20 et 23 sont considéré comme des portes ouvertes et entre 24 et 27 comme des portes fermées. | 1 (20 à 27) (20 à 27) |
| `r` | `g` | `b` | Place uniquement du sol | 1 0 0 |