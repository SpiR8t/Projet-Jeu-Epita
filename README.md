# Projet-Jeu-Epita
Projet de groupe sur la création d'un jeux sur python

# Nécessaire pour modifier le code
Pour contribuer au projet, il est nécessaire de faire différentes choses.
### Créer un environnement python
Il faut créer un environnement python spécifique au projet ou seront installé les librairies nécessaires. 
Pour cela entrer la commade suivante il est possible de mettre le nom que l'on souhaite à la place de projet_prog_s1 :
```python -m venv projet_prog_s1```
Puis on doit activer l'environnement en faisant :
```projet_prog_s1\Scripts\activate```

On peut maintenant installer les librairies nécessaires au projet.

### Installer les librairies nécéssaires
Voici les différentes librairies que notre code utilise, leur utilité, et comment les installer :
- aiortc : utilisée pour faire la connection P2P. Installation :
```pip install aiortc```

- requests : utilisée pour communiquer avec la base de donnée firebase. Installation :
```pip install requests```

- pygame : utilisée pour implémenter tout le fonctionnemment du jeu. Installation :
```pip install pygame```