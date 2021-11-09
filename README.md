# P2_bookshop_scraping

Description
----------
Projet 2 du parcours OpenClassrooms "Developpeur d'appli Python".
Réalisation d'un programme de surveillance des prix des livres de la librairie en ligne "Books to Scrape" (https://books.toscrape.com), en 3 étapes :
- 1 script pour extraire les données d'un livre et les charger dans un fichier .csv
- 1 script pour extraire les données des livres d'une catégorie et les charger dans un fichier .csv
- 1 script pour extraire les données des livres de chaque catégorie, les charger dans un fichier .csv par catégorie et télécharger les images de couverture des livres 


Préalables et déroulement :
-------------------------
Avertissement : Les scripts ont été créés et testés dans un environnement Windows, avec Python3.10.0 et pip 21.2.3
Les commandes suivantes peuvent différer selon votre propre environnement.

Pour commencer, ouvrir un terminal de commande (Git Bash, par exemple). 
Créer le répertoire de travail (commande : mkdir) qui accueillera les scripts Python. 

Puis créer un environnement virtuel à la racine du répertoire de travail (python -m venv env). 

Initialiser Git dans le répertoire de travail (git init). 

Charger, dans votre répertoire de travail, les fichiers déposés sur GitHub (lien : https://github.com/RVLdev/P2_bookshop_scraping.git) :
- script_1livre.py, 
- script_1ktgorie.py, 
- script_bookstoscrape.py, 
- requirements.txt

Activer l'environnement virtuel (. env/Scripts/activate - sous Windows). 
Installer les paquets/modules indiqués dans le fichier requirements.txt (pip install -r requirements.txt). 
Exécuter le(s) script(s) (python script.py). 
Une fois le programme exécuté (un message de fin s'affiche), désactiver l'environnement virtuel (deactivate). 

Le script "script_bookstoscrape.py" dure environ 22 minutes (fibre optique)
Les fichiers .csv et les images de couverture des livres sont créés directement dans le répertoire de travail où vous avez déposé les scripts en Python.
