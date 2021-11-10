import requests
from requests.compat import urljoin
from bs4 import BeautifulSoup
import csv


# url = Product_page_link
url = 'https://books.toscrape.com/catalogue/category/books/childrens_11/index.html'

unecategorie = requests.get(url)
soup = BeautifulSoup(unecategorie.content, 'html.parser')


""" NOMBRE de PAGES dans la CATEGORIE 
(20 livres par page)
"""
books_qty = soup.find_all("strong")[1].text


if (int(books_qty))%20 ==0: 
    nbpages = (int(books_qty))/20
else : nbpages =((int(books_qty))//20)+1
 

"""Liste des URLS des PAGES de la CATEGORIE "childrens" 
"""

liste_urlpages = []
liste_urlpages.append(url) # ajoute la 1ère page de la catégorie

if nbpages > 1:
	for i in range(2,(nbpages+1)):
	    urlpage=url.replace("index", "page-"+str(i))
	    liste_urlpages.append(urlpage) #ajoute les pages >1 
else: 
	pass


"""
liste URLS des LIVRES (de chaque page) de la CATEGORIE

"""

liste_lienboukins = []

for urlp in liste_urlpages:
	pagecategorie = requests.get(urlp)
	soup_pcat = BeautifulSoup(pagecategorie.content, 'html.parser')

	boukins = soup_pcat.find_all("h3")

	for boukin in boukins:
		a = boukin.find('a')
		lien = a['href']
		lienboukin = lien.replace("../../../", 'https://books.toscrape.com/catalogue/')
		liste_lienboukins.append(lienboukin)

""" Récupération des DONNES de chq LIVRE et copie dans CSV
"""
with open ('data_catlivres.csv', 'w', newline='') as csv_file:
		en_tete = ["product_page_url", "universal_product_code (upc)", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]
		writer = csv.DictWriter(csv_file, fieldnames=en_tete, delimiter=',')
		
		writer.writeheader()


for urll in liste_lienboukins:
	livre = requests.get(urll)
	soup_livr = BeautifulSoup(livre.content, 'html.parser')

	""" TITRE  
	"""
	titre = soup_livr.find('h1')
	letitre=titre.text


	""" UPC,  PRICE EXCL, PRICE INCL, AVAILABILITY 
	"""

	valeurs = soup_livr.find_all("td")
	caracteristiques = []
	for valeur in valeurs:
	    caracteristiques.append(valeur.string)
	    
	upc = caracteristiques[0]
	prix_ttc = caracteristiques[3]
	prix_ht = caracteristiques[2]
	nbre_dispo = caracteristiques[5] 


	"""DESCRIPTION 
	"""
	description = soup_livr.find("p", class_="").text

	""" nom CATEGORIE
	"""
	ktgories = soup_livr.find_all('li')
	ktgorie=(ktgories[2].text) 

	""" 
	REVIEW RATING 
	"""
	stars = soup_livr.find("p", class_="star-rating")
	rating = str(stars).split(" ")[2]
	star_rate=(rating[:-5])
	 
	""" 
	lien IMAGE de couverture
	"""
	couverture = soup_livr.find_all("div", class_="item active")
	for couv in couverture:
		img = couv.find('img')
		lien = img['src']
		
		lienimage = urljoin('http://books.toscrape.com', lien)

	# création du FICHIER CSV
	with open ('data_catlivres.csv', 'a', newline='') as csv_file:
		writer = csv.DictWriter(csv_file, fieldnames=en_tete, delimiter=',')
		writer.writerow({"product_page_url":urll, "universal_product_code (upc)":upc, "title":letitre, "price_including_tax":prix_ttc, "price_excluding_tax":prix_ht, "number_available":nbre_dispo, "product_description":description, "category":ktgorie, "review_rating":star_rate, "image_url":lienimage})


