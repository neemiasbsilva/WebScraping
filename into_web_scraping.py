import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from urllib.error import HTTPError
import pandas as pd

def main():
    my_url = 'https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38?Tpk=Graphics%20Card'

    # opening up connection, grabbing the page
    try:
        uClient = uReq(my_url)
    except HTTPError as e:
        print(e)
    page_html = uClient.read()
    uClient.close()

    # html parsing
    page_soup = soup(page_html, "html.parser")
    page_soup.h1
    page_soup.p
    
    # grabs each product
    containers = page_soup.findAll("div", {"class": "item-container"})
    # how many objects find
    print(len(containers))
    product_names = list()
    brands = list()
    shippings = list()
    for container in containers:
        brand = container.a.img["title"]
        title_container = container.findAll("a", {"class": "item-title"})
        product_name = title_container[0].text
        shipping_container = container.findAll("li", {"class": "price-ship"})
        shipping = shipping_container[0].text.strip()

        # print("brand: "+brand)
        # print("product_name: "+product_name)
        # print("shipping: "+ shipping)
        product_names.append(product_name.replace(",", "|"))
        brands.append(brand)
        shippings.append(shipping)

    df = pd.DataFrame({"Product names":product_names,"Brands":brands, "Shippings":shippings})
    print(df.head())
    df.to_csv("Graphics_cards_new_egg.csv")
if __name__ == '__main__':
    main()
