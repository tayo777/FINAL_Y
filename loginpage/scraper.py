from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from django.shortcuts import redirect, render
from .models import AmazonProduct
# Function to extract Product Title
def scrape_amazon(query):
    def get_title(soup):

        try:
            # Outer Tag Object
            title = soup.find("span", attrs={"id":'productTitle'})
            
            # Inner NavigatableString Object
            title_value = title.text

            # Title as a string value
            title_string = title_value.strip()

        except AttributeError:
            title_string = ""

        return title_string

    # Function to extract Product Price
    def get_price(soup):

        try:
            price = soup.find("span", attrs={'id':'priceblock_ourprice'}).string.strip()

        except AttributeError:

            try:
                # If there is some deal price
                price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()

            except:
                price = ""
        return price

    # Function to extract Product Rating
    def get_rating(soup):

        try:
            rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
        
        except AttributeError:
            try:
                rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
            except:
                rating = ""	

        return rating

    # Function to extract Number of User Reviews
    def get_review_count(soup):
        try:
            review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

        except AttributeError:
            review_count = ""	

        return review_count

    # Function to extract Availability Status
    def get_availability(soup):
        try:
            available = soup.find("div", attrs={'id':'availability'})
            available = available.find("span").string.strip()

        except AttributeError:
            available = "Not Available"	
        return available




        # add your user agent 
    HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
    products = []
    page=1
    URL = f"https://www.amazon.com/s?k={query}&page={page}"
    # HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

    # Store the links
    links_list = []

    # Loop for extracting links from Tag Objects
    for link in links:
            links_list.append(link.get('href'))

    d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[]}

    # Loop for extracting product details from each link 
    for link in links_list:
        new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        # Create and save AmazonProduct objects
        product = AmazonProduct(
            title=get_title(new_soup),
            price=get_price(new_soup),
            rating=get_rating(new_soup),
            reviews=get_review_count(new_soup),
            availability=get_availability(new_soup)
        )
        product.save()
        products.append(product)


    return products


   