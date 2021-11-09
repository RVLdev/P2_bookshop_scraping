# Print() : laissés en cas de démonstration
import requests
from requests.compat import urljoin
from bs4 import BeautifulSoup
import csv

url = 'https://books.toscrape.com/catalogue/the-white-cat-and-the-monk-a-retelling-of-the-poem-pangur-ban_865/index.html'
# = url de la page produit

livre = requests.get(url)
soup = BeautifulSoup(livre.content, 'html.parser')


# TITRE du livre 
titre = soup.find('h1')
letitre=titre.text
print(letitre)


# UPC,  PRICE EXCL, PRICE INCL, AVAILABILITY 

valeurs = soup.find_all("td")
caracteristiques = []
for valeur in valeurs:
    caracteristiques.append(valeur.string)

upc = caracteristiques[0]
prix_ttc = caracteristiques[3]
prix_ht = caracteristiques[2]
nbre_dispo = caracteristiques[5]

print (upc)
print(prix_ttc)
print(prix_ht)
print(nbre_dispo)


# DESCRIPTION 

description = soup.find("p", class_="").text
print(description)


# CATEGORIE 

ktgories = soup.find_all('li')
ktgorie=(ktgories[2].text)
print(ktgorie)


# REVIEW RATING 

stars = soup.find("p", class_="star-rating")
rating = str(stars).split(" ")[2]
star_rate=(rating[:-5])
print(star_rate)


# IMAGE : récupération de l'url de l'image de couverture

couverture = soup.find_all("div", class_="item active")
for couv in couverture:
	img = couv.find('img')
	lien = img['src']
	lienimage = urljoin('https://books.toscrape.com', lien)
	print(lienimage)


# création du fichier csv et alimentation

with open ('data_livre.csv', 'w', newline='') as csv_file:
	en_tete = ["product_page_url", "universal_product_code (upc)", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]
	writer = csv.DictWriter(csv_file, fieldnames=en_tete, delimiter=',')
	
	writer.writeheader()
	writer.writerow({"product_page_url":url, "universal_product_code (upc)":upc, "title":letitre, "price_including_tax":prix_ttc, "price_excluding_tax":prix_ht, "number_available":nbre_dispo, "product_description":description, "category":ktgorie, "review_rating":star_rate, "image_url":lienimage})

