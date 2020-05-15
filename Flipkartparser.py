'''Details of the project - This is a python project that takes the item you want to search on flipkart as input generates and 
prints the URL of that product. Then makes a .csv file of the same name as the input.This file has the headings- Product_Name, Pricing, Ratings and Link
with the entities of flipkart's first page below it. Note- In case you want to verify if what was parsed is correct by opening the URL
use incognito browser so your cache and your history doesn't affect the findings of the page.
'''
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
sear=str(input())
my_url= (f'https://www.flipkart.com/search?q={sear.replace(" ","+")}')
print(my_url)
uClient = uReq(my_url)
page = uClient.read()
uClient.close()
page_soup = soup(page, "lxml")
containers = page_soup.findAll("div", {"class": "_3O0U0u"})
filename = f"{sear}.csv"
f = open(filename, "w")
headers = "Product_Name, Pricing, Ratings, Link \n"
f.write(headers)
for container in containers:
    name_container1 = container.findAll("div",{"class": "_3wU53n"})
    link_container = container.findAll("a")
    for i in range(len(link_container)):
        link_container[i]=link_container[i].get('href')
    seen = set()
    seen_add = seen.add
    link_container1 = [x for x in link_container if not (x in seen or seen_add(x))]
    name_container2 = container.findAll("div",{"class": "_3liAhj"})
    price_container = container.findAll("div", {"class": "_1vC4OE"})
    rating_container = container.findAll("div", {"class": "niH0FQ"})
    for i in range(len(price_container)):
        try:
            product_name =name_container1[i].text
        except:
            product_name = name_container2[i].img['alt']
        link=str("https://www.flipkart.com"+link_container1[i])
        link.replace(" ","+")
        price = price_container[i].text.strip()
        trim_price = ''.join(price.split(','))
        rm_rupee = trim_price.split('₹')
        add_rs_price = "Rs." + rm_rupee[1]
        final_price = add_rs_price
        try:
            rating = rating_container[i].text
            split_rating = rating.split(" ")
            split_rating = split_rating[0].split("(")
            final_rating = split_rating[0].split(",")
        except:
            final_rating="Not Rated"
        f.write(str(product_name).replace(",", "|") + "," + final_price + "," + final_rating[0] + "," + link + "\n")
f.close()
from subprocess import Popen
p = Popen(filename, shell=True)
