import requests
from requests.compat import urljoin
from bs4 import BeautifulSoup
import csv

url = 'http://books.toscrape.com/catalogue/the-white-cat-and-the-monk-a-retelling-of-the-poem-pangur-ban_865/index.html'
# url = Product_page_link

livre = requests.get(url)
soup = BeautifulSoup(livre.content, 'html.parser')

""" TITRE : ok """
titre = soup.find('h1')
letitre=titre.text
print(letitre)


"""
UPC,  PRICE EXCL, PRICE INCL, AVAILABILITY : ok

N.B. 
les <th> servent à repérer l'ordre des données 
et celles qui ne seront pas utilisées
nom_items = soup.find_all("th")
print(nom_items) 	=> faire del [1][3][-1]
"""

valeurs = soup.find_all("td")
caracteristiques = []
for valeur in valeurs:
    caracteristiques.append(valeur.string)
    
del caracteristiques[1]
del caracteristiques[3]
del caracteristiques[-1]
print(caracteristiques)

upc = caracteristiques[0]
prix_ttc = caracteristiques[2]
prix_ht = caracteristiques[1]
nbre_dispo = caracteristiques[3]

print (upc)
print(prix_ttc)
print(prix_ht)
print(nbre_dispo)


"""
DESCRIPTION = ok
découvert par hasard, dans expression : soup.find("p", class_="") 
class_=""   indique un "p" sans "class"
"""
description = soup.find("p", class_="").text
print(description)


""" CATEGORIE : ok
N.B. orthographe "ktgorie(s)" en prévision usage du mot "categorie(s)" 
dans un script de la suite du projet
"""
ktgories = soup.find_all('li')
ktgorie=(ktgories[2].text)
print(ktgorie)


""" 
REVIEW RATING : ok (re-testé avec livres 1 et 3 étoiles)
le seul endroit où il apparaît = L184 du code HTML
 <p class_="star-rating Four">
"""
stars = soup.find("p", class_="star-rating")
rating = str(stars).split(" ")[2]
print(rating)
star_rate=(rating[:-5])
print(star_rate)


""" 
IMAGE : récup lien image - lien testé : ok
"""
couverture = soup.find_all("div", class_="item active")

for couv in couverture:
	img = couv.find('img')
	lien = img['src']
	
	lienimage = urljoin('http://books.toscrape.com', lien)
	print(lienimage)

"""
nouvel ESSAI (v 20/10) création CSV
	newline=''  ==> évite l'insertion auto d'une ligne vide 
	entre les lignes de données
	writer.writeheader()
	PB : crée une ligne pour les entêtes en dessous des titres de 
	colonnes (elles-même nommées col1, col2, etc)
	
"""
# création du fichier csv  
with open ('data_livre.csv', 'w', newline='') as csv_file:
	en_tete = ["product_page_url", "universal_product_code (upc)", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]
	writer = csv.DictWriter(csv_file, fieldnames=en_tete, delimiter=',')
	
	writer.writeheader()
	writer.writerow({"product_page_url":url, "universal_product_code (upc)":upc, "title":letitre, "price_including_tax":prix_ttc, "price_excluding_tax":prix_ht, "number_available":nbre_dispo, "product_description":description, "category":ktgorie, "review_rating":star_rate, "image_url":lienimage})


""""
AUTRE METHODE ne fonctionne pas telle quelle(==>fichiers-tests py et csv supprimés) ; insère un séparateur 
apres chq caractère des données de "data_livre"

en_tete = ["product_page_url", "universal_product_code (upc)", "title", "price_including_tax", "price_excluding_tax", 
"number_available", "product_description", "category", "review_rating", "image_url"]
data_livre = [url, upc, letitre, prix_ttc, prix_ht, nbre_dispo, description, ktgorie, star_rate, lienimage]

modèle :
------
header = ['row1', 'row2', 'row3']
some_list = [1, 2, 3]
with open('test.csv', 'wt', newline ='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(i for i in header)
    for j in some_list:
        writer.writerow(j)

"""
