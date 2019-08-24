# Import Dependecies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
import time

# Initialize browser
def init_browser():
        
    execut_path = {'executable_path': 'C:\Tools\chromedriver.exe'}
    return Browser('chrome', **execut_path, headless=True)


# Create Mission to Mars global dictionary that can be imported into Mongo
mars_info = {}

# NASA MARS NEWS


def scrape_mars_news():
    try:
        # Initialize browser
        browser = init_browser()

       # browser.is_element_present_by_css("div.content_title", wait_time=1)

        # Visit Nasa news url through splinter module
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        # HTML Object
        html = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')

        # Retrieve the latest element that contains news title and news_paragraph
        news_title = soup.find('div', class_='content_title').find('a').text
        news_para = soup.find('div', class_='article_teaser_body').text

        # Dictionary entry from MARS NEWS
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_para
    finally:
        return mars_info


# FEATURED IMAGE
def scrape_mars_image():
    try:
        # Initialize browser
        browser = init_browser()

        browser.is_element_present_by_css("img.jpg", wait_time=1)

        # Visit Mars Space Images through splinter module
        image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        # Visit Mars Space Images through splinter module
        browser.visit(image_url_featured)

        # HTML Object
        html_image = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_image, 'html.parser')

        # Retrieve background-image url from style tag
        featured_image_url = soup.find('article')['style'].replace('background-image: url(', '').replace(');', '')[1:-1]

        # Website Url
        main_url = 'https://www.jpl.nasa.gov'

        # Concatenate website url with scrapped route
        featured_image_url = main_url + featured_image_url

        # Display full link to featured image
        featured_image_url

        # Dictionary entry from FEATURED IMAGE
        mars_info['featured_image_url'] = featured_image_url
    finally:
        return mars_info


def scrape_mars_weather():
    try:
        # Initialize browser
        browser = init_browser()
        browser.is_element_present_by_css("div", wait_time=1)

        # Visit Mars Weather Twitter through splinter module
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)

        # HTML Object
        html_weather = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_weather, 'html.parser')

        # Find all elements that contain tweets
        latest_tweets = soup.find_all('div', class_='js-tweet-text-container')

        # Retrieve all elements that contain news title in the specified range
        # Look for entries that display weather related words to exclude non weather related tweets
        for tweet in latest_tweets:
            weather_tweet = tweet.find('p').text
            if 'Sol' and 'pressure' in weather_tweet:
                print(weather_tweet)
                break
            else:
                pass

        # Dictionary entry from WEATHER TWEET
        mars_info['weather_tweet'] = weather_tweet
    finally:
        return mars_info


# Hemispheres images
def scrape_mars_hemispheres():
    try:
        # Initialize browser
        browser = init_browser()

        # Visit hemispheres website through splinter module
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        # HTML Object
        html_hemispheres = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_hemispheres, 'html.parser')

        # Retreive all items that contain mars hemispheres information
        items = soup.find_all('div', class_='item')

        # Create empty list for hemisphere urls
        hiu = []

        # Store the main_ul
        hemispheres_main_url = 'https://astrogeology.usgs.gov'

        # Loop through the items previously stored
        for i in items:
            # Store title
            title = i.find('h3').text

            # Store link that leads to full image website
            partial_img_url = i.find('a', class_='itemLink product-item')['href']

            # Visit the link that contains the full image website
            browser.visit(hemispheres_main_url + partial_img_url)

            # HTML Object of individual hemisphere information website
            partial_img_html = browser.html

            # Parse HTML with Beautiful Soup for every individual hemisphere information website
            soup = BeautifulSoup(partial_img_html, 'html.parser')

            # Retrieve full image source
            img_url = hemispheres_main_url + \
                soup.find('img', class_='wide-image')['src']

            # Append the retreived information into a list of dictionaries
            hiu.append({"title": title, "img_url": img_url})

        mars_info['hiu'] = hiu
    finally:
        return mars_info

# Mars Facts
def scrape_mars_facts():
    try:

        facts_url = 'http://space-facts.com/mars/'
        table = pd.read_html(facts_url)
        df = table[1]
        df.columns = ['Index', 'Measurement']

        df.to_html("mars_facts")
        mars_info['mars_facts'] = mars_facts
    finally:
        return(mars_info)    
