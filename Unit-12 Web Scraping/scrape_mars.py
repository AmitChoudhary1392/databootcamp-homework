### Mission to Mars- Scraping

# Import Dependencies
import os
from os import path
from bs4 import BeautifulSoup as bs
import pandas as pd
import splinter
from splinter import Browser

def init_browser():
     # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    return browser

mars_data={}

def scrape_all():

    ####1. NASA Mars News
            
    browser= init_browser()
    # Url of page to scrape recent Mars headline from NASA news site
    url_news='https://mars.nasa.gov/news/'

    # Browser visit
    browser.visit(url_news)

    # Create a Beautiful Soup object
    html = browser.html
    news_soup = bs(html, 'html.parser')

    #Extract news title
    news_title= news_soup.find('div', class_='content_title').find('a').text
    
    #Extratc news paragraph
    news_para= news_soup.find('div', class_='article_teaser_body').text
    

    # ###2. JPL Mars Space Images - Featured Image

    # Url of page to scrape recent Mars images from NASA site
    url_img= 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    #define base_url
    base_url='https://www.jpl.nasa.gov'

    # Browser visit
    browser.visit(url_img)

    # Create a Beautiful Soup object
    html = browser.html
    img_soup = bs(html, 'html.parser')

    #get the image url from the soup object
    img_url=img_soup.find('div',class_='carousel_items').find('a').attrs['data-link']

    #create new url for enlarged image
    img_url1= base_url+img_url

    browser.visit(img_url1)

    # Create a Beautiful Soup object
    html = browser.html
    img_soup2 = bs(html, 'html.parser')

    #get url for large size featured image
    img_url2=img_soup2.find_all('figure', class_='lede')[0].a['href']

    #featured image url
    featured_image_url= base_url + img_url2

 
    # ###3. Mars Weather

    #Visit the Mars Weather twitter account
    Tweet_url='https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module
    browser.visit(Tweet_url)

    #create BeautifulSoup object
    html=browser.html
    tweet_soup=bs(html,'html.parser')

    # Extract title text
    mars_weather = tweet_soup.find('p',class_='TweetTextSize').text
    

    # ###4. Mars Facts

    # Visit the Mars Facts webpage
    facts_url='https://space-facts.com/mars/'

    #read table from facts page
    fact_table=pd.read_html(facts_url)

    #Create Dataframe to store table data
    df = fact_table[0]
    df.columns = ['Features','Values']

    #convert dataFrame to HTML table
    html_table = df.to_html().replace('\n','')
    

    # ###5. Mars Hemispheres

    # USGS Astrogeology site
    USGS_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    base_url2="https://astrogeology.usgs.gov"


    #browser visit
    browser.visit(USGS_url)
    html = browser.html

    #create beautiful soup object
    hem_soup = bs(html, 'html.parser')

    #get urls for each page
    url_obj = hem_soup.find_all('div', class_='item')

    #define variable to store titles and images data
    hemisphere_img_urls=[]

    for item in url_obj:
        title = item.find('h3').text    #extract title of hemisphere
        
        browser.click_link_by_partial_text(title)       #visit hemisphere detail page
        html = browser.html
        soup = bs(html, 'html.parser')
        
        hemisphere_img= soup.find('div',class_='downloads')     #extract enlarged image url
        hemisphere_img_url=hemisphere_img.find('a')['href']
        
        img_data=dict({'title':title, 'img_url':hemisphere_img_url})
        hemisphere_img_urls.append(img_data)
        
        browser.back()
        
    mars_data={'news_title':news_title,
                'news_paragraph': news_para,
                'featured_image_url':featured_image_url,
                'mars_weather': mars_weather,
                'mars_facts':html_table,
                'hemisphere_img_urls': hemisphere_img_urls
                }
    
    browser.quit()

    return mars_data