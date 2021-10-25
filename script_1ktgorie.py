"""Id pour script2"""


#requirements
import requests
from requests.compat import urljoin
from bs4 import BeautifulSoup
import csv


# url = Product_page_link
url = 'https://books.toscrape.com/catalogue/category/books/childrens_11/index.html'

unecategorie = requests.get(url)
soup = BeautifulSoup(unecategorie.content, 'html.parser')


"""	recherche nombre de pages dans la catégorie
"""
pages_cat = soup.find_all("strong")[1].text
print(pages_cat)


if (int(pages_cat))%20 ==0: 
    nbpages = (int(pages_cat))/20
else : nbpages =((int(pages_cat))//20)+1

print(nbpages)


"""création et alimentation de la liste des urls des pages de la catégorie "childrens" 
"""

liste_urlpages = []
liste_urlpages.append(url)

if nbpages > 1:
	for i in range(2,(nbpages+1)):
	    urlpage=url.replace("/index.html", "/page-"+str(i)+".html")
	    liste_urlpages.append(urlpage)
	print(liste_urlpages)

else: print(liste_urlpages)

"""
pour chaque page de catégorie (liens des pages), 
récupération des liens des livres (de chaque page)

23/10 blocage au niveau des liens livres (erreur 404 not found)
	corr. identation "print(liste_lienboukins)"
	corr. urljoin : http => https

"""

liste_lienboukins = []

for urlp in liste_urlpages:
	pagecategorie = requests.get(urlp)
	soup_pcat = BeautifulSoup(pagecategorie.content, 'html.parser')

	boukins = soup_pcat.find_all("h3")

	for boukin in boukins:
		a = boukin.find('a')
		lien = a['href']
		lienboukin = urljoin('https://books.toscrape.com/catalogue', lien)
		liste_lienboukins.append(lienboukin)
	print(liste_lienboukins)

"""
pour chaque lien de livre, récupérer les données dans csv
voir fichier 'brouillon-script1livre.py'
"""

for urll in liste_lienboukins:
	livre = requests.get(urll)
	soup_livr = BeautifulSoup(livre.content, 'html.parser')

	""" TITRE : ok """
	titre = soup_livr.find('h1')
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

	valeurs = soup_livr.find_all("td")
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
	description = soup_livr.find("p", class_="").text
	print(description)


	""" CATEGORIE : ok
	N.B. orthographe "ktgorie(s)" en prévision usage du mot "categorie(s)" 
	dans un script de la suite du projet
	"""
	ktgories = soup_livr.find_all('li')
	ktgorie=(ktgories[2].text)
	print(ktgorie)


	""" 
	REVIEW RATING : ok (re-testé avec livres 1 et 3 étoiles)
	le seul endroit où il apparaît = L184 du code HTML
	 <p class_="star-rating Four">
	"""
	stars = soup_livr.find("p", class_="star-rating")
	rating = str(stars).split(" ")[2]
	print(rating)
	star_rate=(rating[:-5])
	print(star_rate)


	""" 
	IMAGE : récup lien image - lien testé : ok
	"""
	couverture = soup_livr.find_all("div", class_="item active")

	for couv in couverture:
		img = couv.find('img')
		lien = img['src']
		
		lienimage = urljoin('http://books.toscrape.com', lien)
		print(lienimage)

	
	# création du fichier csv  
	with open ('data_catlivr.csv', 'w', newline='') as csv_file:
		en_tete = ["product_page_url", "universal_product_code (upc)", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]
		writer = csv.DictWriter(csv_file, fieldnames=en_tete, delimiter=',')
		
		writer.writeheader()
		writer.writerow({"product_page_url":url, "universal_product_code (upc)":upc, "title":letitre, "price_including_tax":prix_ttc, "price_excluding_tax":prix_ht, "number_available":nbre_dispo, "product_description":description, "category":ktgorie, "review_rating":star_rate, "image_url":lienimage})


