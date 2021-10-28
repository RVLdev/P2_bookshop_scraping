import requests
from requests.compat import urljoin
from bs4 import BeautifulSoup
import csv

url = 'https://books.toscrape.com/index.html'

website_requested = requests.get(url)
soup = BeautifulSoup(website_requested.content, 'html.parser')

categories_pagination = soup.find("div", class_="side_categories").find_all("li")

"""List the links of all categories
"""
categories_links_list = []

for categ in categories_pagination:
    a = categ.find('a')
    link = a['href']
    categories_links = urljoin('https://books.toscrape.com/', link)
    categories_links_list.append(categories_links)
del categories_links_list[0]    


# List the name of each category
list1 = []
list2 = []
categories_names_list = []

for li in categories_pagination:
    a = li.find('a')
    list1.append(a['href'][25:-13])
    list2.append(a['href'][25:-14])
    
for i in list1[1:9]:    
    categories_names_list.append(i)
for j in list2[9:51]:
    categories_names_list.append(j)
    

# create CSV file for each category
csv_list = []
for name in categories_names_list:
    csv_file.append(name+".csv")

for file in csv_list:
    with open (file, 'w', newline='') as csv_file:
        en_tete = ["product_page_url", "universal_product_code (upc)", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]
        writer = csv.DictWriter(csv_file, fieldnames=en_tete, delimiter=',')
        
        writer.writeheader()


""" CATEGORIES PAGES
"""
for categorie_link in categories_links_list:
    categories_links_requested = requests.get(categorie_link)
    soup_categories_links=BeautifulSoup(categories_links_requested.content, 'html.parser')

    # calcul nb pages 
    pages_cat = soup_categories_links.find_all("strong")[1].text

    if (int(pages_cat))%20 ==0: 
        nbpages = (int(pages_cat))/20
    else : nbpages =((int(pages_cat))//20)+1

    """Liste des URLS des PAGES des CATEGORIES
    """
    liste_urlpages = []
    liste_urlpages.append(categorie_link) # ajoute la 1ère page de la catégorie

    if nbpages > 1:
        for i in range(2,(nbpages+1)):
            urlpage=categorie_link.replace("index", "page-"+str(i))
            liste_urlpages.append(urlpage) #ajoute les pages >1 
    else: 
        pass
    

    # liste URLS des LIVRES = OK (dernier livre vérifié)
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


    """ BOOKS DATA
    """

    for urll in liste_lienboukins:
        livre = requests.get(urll)
        soup_livr = BeautifulSoup(livre.content, 'html.parser')

        # Title

        titre = soup_livr.find('h1')
        letitre=titre.text


        # UPC, Price excl. Price Incl. Availability 

        valeurs = soup_livr.find_all("td")
        caracteristics = []
        for valeur in valeurs:
            caracteristics.append(valeur.string)
            
        upc = caracteristics[0]
        prix_ttc = caracteristics[3]
        prix_ht = caracteristics[2]
        nbre_dispo = caracteristics[5]


        # Description 

        description = soup_livr.find("p", class_="")
        if description !=None:
            description = description.text
        else: 
            pass
        
        # Category
        
        ktgories = soup_livr.find_all('li')
        ktgorie=(ktgories[2].text)
         
        # Review rating 
        
        stars = soup_livr.find("p", class_="star-rating")
        rating = str(stars).split(" ")[2]
        star_rate=(rating[:-5])
        
        # link to cover page picture
        
        cover_page = soup_livr.find_all("div", class_="item active")
        for c_page in cover_page:
            pict = c_page.find('img')
            picture_link = pict['src']
            
            cover_page_link = urljoin('http://books.toscrape.com', picture_link)


        # CSV fill-in
        for file in csv_list: 
        with open (file, 'a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=en_tete, delimiter=',')
            writer.writerow({"product_page_url":urll, "universal_product_code (upc)":upc, "title":letitre, "price_including_tax":prix_ttc, "price_excluding_tax":prix_ht, "number_available":nbre_dispo, "product_description":description, "category":ktgorie, "review_rating":star_rate, "image_url":cover_page_link})

