import requests
from requests.compat import urljoin
from bs4 import BeautifulSoup
import csv

url = 'https://books.toscrape.com/index.html'

website_requested = requests.get(url)
soup = BeautifulSoup(website_requested.content, 'html.parser')

categories_pagination = soup.find("div", class_="side_categories").find_all("li")

#Links of all categories

categories_links_list = []

for categ in categories_pagination:
    a = categ.find('a')
    link = a['href']
    categories_links = urljoin('https://books.toscrape.com/', link)
    categories_links_list.append(categories_links)
del categories_links_list[0]    


""" starting from CATEGORIES' links
"""
for category_link in categories_links_list:
    categories_links_requested = requests.get(category_link)
    soup_categories_links=BeautifulSoup(categories_links_requested.content, 'html.parser')

    # Category name
    category_pagination = soup_categories_links.find('li', class_='active')
    category_name = category_pagination.text
    
    # CSV creation
    with open (category_name+".csv", 'w', newline='') as csv_file:
                csv_header = ["product_page_url", "universal_product_code (upc)", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]
                writer = csv.DictWriter(csv_file, fieldnames=csv_header, delimiter=',')
                writer.writeheader()
                
                
    # calculate the number of pages (in a category) 
    pages_cat = soup_categories_links.find_all("strong")[1].text

    if (int(pages_cat))%20 ==0: 
        nbpages = (int(pages_cat))/20
    else : nbpages =((int(pages_cat))//20)+1

    # Urls of CATEGORIES PAGES 
    
    urlpages_list = []
    urlpages_list.append(category_link) # ajoute la 1ère page de la catégorie

    if nbpages > 1:
        for i in range(2,(nbpages+1)):
            urlpage=category_link.replace("index", "page-"+str(i))
            urlpages_list.append(urlpage) #ajoute les pages >1 
    else: 
        pass
    

    # Urls of BOOKS
    books_links_list = []

    for urlp in urlpages_list:
        categories_pages_requested = requests.get(urlp)
        soup_pcat = BeautifulSoup(categories_pages_requested.content, 'html.parser')

        books_pagination = soup_pcat.find_all("h3")

        for book in books_pagination:
            a = book.find('a')
            b_link = a['href']
            book_link = b_link.replace("../../../", 'https://books.toscrape.com/catalogue/')
            books_links_list.append(book_link)


    """ DATA from books
    """

    for urll in books_links_list:
        product = requests.get(urll)
        soup_product = BeautifulSoup(product.content, 'html.parser')

        # Title

        title_pagination = soup_product.find('h1')
        title=title_pagination.text


        # UPC, Price excl. Price Incl. Availability 

        values_pagination = soup_product.find_all("td")
        caracteristics = []
        for value in values_pagination:
            caracteristics.append(value.string)
            
        upc = caracteristics[0]
        price_incl = caracteristics[3]
        price_excl = caracteristics[2]
        nbr_available = caracteristics[5]


        # Description 

        description_pagination = soup_product.find("p", class_="")
        if description_pagination !=None:
            description = description_pagination.text
        else: 
            description = "No description"
        
        # Category
        
        product_category_pagination= soup_product.find_all('li')
        product_category=(product_category_pagination[2].text)
         
        # Review rating 
        
        stars = soup_product.find("p", class_="star-rating")
        rating = str(stars).split(" ")[2]
        star_rate=(rating[:-5])
        
        # link to cover page picture
        
        cover_page_pagination = soup_product.find_all("div", class_="item active")
        for c_page in cover_page_pagination:
            pict = c_page.find('img')
            picture_link = pict['src']
            
            cover_page_link = urljoin('http://books.toscrape.com', picture_link)


        # CSV fill-in
       
        with open (file, 'a', newline='') as csv_file:
            csv_header = ["product_page_url", "universal_product_code (upc)", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"]
            writer = csv.DictWriter(csv_file, fieldnames=csv_header, delimiter=',')
            writer.writeheader()
            writer.writerow({"product_page_url":urll, "universal_product_code (upc)":upc, "title":title, "price_including_tax":price_incl, "price_excluding_tax":price_excl, "number_available":nbr_available, "product_description":description, "category":product_category, "review_rating":star_rate, "image_url":cover_page_link})

