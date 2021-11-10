import requests
from requests.compat import urljoin
from bs4 import BeautifulSoup
import csv

URL = 'https://books.toscrape.com/index.html'
website_requested = requests.get(url=URL)
soup = BeautifulSoup(website_requested.content, 'html.parser')
CSV_HEADER = ["product_page_url", "universal_product_code (upc)", "title",
              "price_including_tax", "price_excluding_tax", "number_available",
              "product_description", "category", "review_rating", "image_url"]


def get_categories_list(soup):
    categories_pagination = soup.find("div", class_="side_categories")
    categories_links_list = []
    li_cat_pagination = categories_pagination.find_all("li")
    for li in li_cat_pagination:
        a = li.find('a')
        link = a['href']
        categories_links = urljoin('https://books.toscrape.com/', link)
        categories_links_list.append(categories_links)
    del categories_links_list[0]
    return categories_links_list


def get_category_name(category_pagination):
    return(category_pagination.text)


def get_nb_pages(books_qty):
    if (int(books_qty)) % 20 == 0:
        return(int(books_qty))/20
    return((int(books_qty))//20)+1


def get_url_categories_pages_list(category_link, nbpages):
    urlpages_list = []
    urlpages_list.append(category_link)

    if nbpages > 1:
        for i in range(2, (nbpages+1)):
            urlpage = category_link.replace("index", "page-"+str(i))
            urlpages_list.append(urlpage)
    return urlpages_list


def create_csv_file(category_name, csv_header=CSV_HEADER):
    with open(category_name+".csv", 'w', newline='',
              encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_header, delimiter=',')
        writer.writeheader()


def get_urls_books(urlpages_list):
    books_links_list = []
    for urlp in urlpages_list:
        categories_pages_requested = requests.get(urlp)
        soup_pcat = BeautifulSoup(categories_pages_requested.content,
                                  'html.parser')
        books_pagination = soup_pcat.find_all("h3")
        for book in books_pagination:
            a = book.find('a')
            b_link = a['href']
            book_link = b_link.replace("../../../",
                                       'https://books.toscrape.com/catalogue/')
            books_links_list.append(book_link)
    return books_links_list


def data_dict():
    return {
        "product_page_url": None,
        "universal_product_code (upc)": None,
        "title": None,
        "price_including_tax": None,
        "price_excluding_tax": None,
        "number_available": None,
        "product_description": None,
        "category": None,
        "review_rating": None,
        "image_url": None
    }


def get_book_data_and_save(books_links_list, category_name,
                           csv_header=CSV_HEADER):

    def get_title(title_pagination):
        return(title_pagination.text)

    def get_upc(values_pagination):
        caracteristics = []
        for value in values_pagination:
            (caracteristics.append(value.string))
        return(caracteristics[0])

    def get_price_inc_tax(values_pagination):
        caracteristics = []
        for value in values_pagination:
            (caracteristics.append(value.string))
        return(caracteristics[3])

    def get_price_excl_tax(values_pagination):
        caracteristics = []
        for value in values_pagination:
            (caracteristics.append(value.string))
        return(caracteristics[2])

    def get_availability(values_pagination):
        caracteristics = []
        for value in values_pagination:
            (caracteristics.append(value.string))
        return(caracteristics[5])

    def get_descripton(description_pagination):
        if description_pagination is not None:
            return(description_pagination.text)
        return("No description")

    def get_category(product_category_pagination):
        return((product_category_pagination[2].text))

    def get_rating(stars):
        return((str(stars).split(" ")[2])[:-5])

    def get_cover_page(cover_page_pagination):
        pict = cover_page_pagination.find('img')
        picture_link = pict['src']
        return(urljoin('https://books.toscrape.com', picture_link))

    def get_picture_name(urll):
        return(urll.replace("https://books.toscrape.com/catalogue/", ""
                            ).replace("/index.html", "").replace(
                            ":", " ").replace("/", " ").replace(
                            '"', "'").replace("*", "_").replace(
                            "?", ""))

    def downloading_cover_page_picture(picture_name):
        image = open(picture_name+".jpg", "wb")
        image.write(image_requested.content)
        image.close()

    for urll in books_links_list:
        data = data_dict()
        data['product_page_url'] = urll
        product = requests.get(urll)
        soup_product = BeautifulSoup(product.content, 'html.parser')

        # Title
        title_pagination = soup_product.find('h1')
        data["title"] = get_title(title_pagination)

        # UPC, Price excl. Price Incl. Availability
        values_pagination = soup_product.find_all("td")

        data["universal_product_code (upc)"] = get_upc(values_pagination)

        data["price_including_tax"] = get_price_inc_tax(values_pagination)

        data["price_excluding_tax"] = get_price_excl_tax(values_pagination)

        data["number_available"] = get_availability(values_pagination)

        # Description
        description_pagination = soup_product.find("p", class_="")
        data["product_description"] = get_descripton(description_pagination)

        # Category
        product_category_pagination = soup_product.find_all('li')
        data["category"] = get_category(product_category_pagination)

        # Review rating
        stars = soup_product.find("p", class_="star-rating")
        data["review_rating"] = get_rating(stars)

        # link to cover page picture
        cover_page_pagination = soup_product.find("div", class_="item active")
        data["image_url"] = get_cover_page(cover_page_pagination)

        # Naming and downloading the cover page picture
        picture_name = get_picture_name(urll)
        image_requested = requests.get(data["image_url"])
        downloading_cover_page_picture(picture_name)

        # CSV fill-in
        fill_in_csv_file(category_name, data, csv_header=CSV_HEADER)


def fill_in_csv_file(category_name, data, csv_header=CSV_HEADER):
    with open(category_name+".csv", 'a', newline='',
              encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_header, delimiter=',')
        writer.writerow(data)


def main(soup):

    # Links of all categories
    categories_links_list = get_categories_list(soup)

    # Categories : name, number of pages, url
    for category_link in categories_links_list:
        categories_links_requested = requests.get(category_link)
        soup_categories_links = BeautifulSoup(categories_links_requested
                                              .content, 'html.parser')

        # Category name
        category_pagination = soup_categories_links.find('li', class_='active')
        category_name = get_category_name(category_pagination)

        # calculate the number of pages (in a category)
        books_qty = soup_categories_links.find_all("strong")[1].text
        nbpages = get_nb_pages(books_qty)

        # Urls of Categories pages
        urlpages_list = get_url_categories_pages_list(category_link, nbpages)

        # CSV creation - per category
        create_csv_file(category_name)

        # Urls of books
        books_links_list = get_urls_books(urlpages_list)

        # Product page:data and picture
        get_book_data_and_save(books_links_list, category_name,
                               csv_header=CSV_HEADER)


main(soup)


print("Your request has come to its end")
