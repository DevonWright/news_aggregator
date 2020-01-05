import os
import json 
import requests
from article import Article
from bs4 import BeautifulSoup
from textblob import TextBlob

def nytimes_scraper(url):
    limit = 3  # Used to limit the amount of articles to be scraped

    # Use Requests to get content from webpage
    website_domain = 'https://www.nytimes.com'
    response = requests.get(url)

    # Use Beautiful Soup to parse HTML and find articles
    soup = BeautifulSoup(response.content, 'html5lib')
    articles = soup.find_all('div', class_='css-1l4spti')

    # Store the title, link, and contents of each article in a list
    usable_articles = []
    for index, article in zip(range(limit), articles):
        this_article = Article()

        # Get article title
        this_article.title = article.find('h2').get_text()

        # Get article link
        this_article.link = website_domain + article.find('a')['href']

        # Get divisions (div's) from the article that are related to the article story.
        response = requests.get(this_article.link)
        soup = BeautifulSoup(response.content, 'html5lib')
        divisions = soup.find_all('div', class_='css-1fanzo5 StoryBodyCompanionColumn')
        
        # Get paragraphs from each div
        content_from_each_div = []
        for div in divisions: 
            paragraphs = div.find_all('p')

            # Join all the paragraphs from this div
            div_content = []
            for paragraph in paragraphs:
                div_content.append(paragraph.get_text())
            div_content = " ".join(div_content)
            content_from_each_div.append(div_content) 

        # Join all div contents together
        this_article.content = " ".join(content_from_each_div)
        usable_articles.append(this_article)

    return usable_articles

def huffpost_scraper(url):
    limit = 3  # Used to limit the amount of articles to be scraped.
    
    # Use Requests to get content for webpage
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}  # This page will reject GET requests that do not identify a User-Agent.
    response = requests.get(url, headers=headers)

    # Use Beautiful Soup to parse HTML and find articles
    soup = BeautifulSoup(response.content, 'html5lib')
    articles = soup.find_all('div', class_='zone__content')[2].find_all('div', class_="card")
    
    # Store the title, link, and contents of each article in a list
    usable_articles = []
    for index, article in zip(range(limit), articles):
        if article.find('h2') == None:
            continue
        else:
            this_article = Article()

            # Get article title
            this_article.title = article.find('h2').get_text()

            # Get article link
            this_article.link = article.find('a')['href']

            # Get divisions (div's) from the article that are related to the article story.
            response = requests.get(this_article.link, headers=headers)
            soup = BeautifulSoup(response.content, 'html5lib')
            divisions = soup.find_all('div', class_='content-list-component yr-content-list-text text')
            
            # Get content from each div
            content = []
            for div in divisions:
                if div.find('p') == None:
                    continue
                else:
                    content.append(div.find('p').get_text())

            # Join all div content together
            this_article.content = " ".join(content)
            usable_articles.append(this_article)

    return usable_articles

def apnews_scraper(url):
    limit = 10  # Will not find articles equal to the limit due to inconsistent HTML.
    website_domain = 'https://apnews.com'

    # Use Requests to get content for webpage
    response = requests.get(url)

    # Use Beautiful Soup to parse HTML and find articles
    soup = BeautifulSoup(response.content, 'html5lib')
    articles = soup.find_all('article', class_='feed')[0].find_all('a')  # Class names on this site is inconsistent, find all hyperlinks.

    # Store the title, link, and contents of each article in a list
    usable_articles = []
    for index, article in zip(range(limit), articles):
        # If the hypelink element contains a h1 element it is a link to an article.
        if article.find('h1') == None:
            continue
        else:
            this_article = Article()

            # Get article title
            this_article.title = article.find('h1').get_text()

            # Get article link
            this_article.link = website_domain + article['href']

            # Get paragraphs from the article that are related to the article story.
            response = requests.get(this_article.link)
            soup = BeautifulSoup(response.content, 'html5lib')
            paragraphs = soup.find_all('p')

            # Get content from each paragraph
            content = []
            for paragraph in paragraphs:
                content.append(paragraph.get_text())

            # Join all paragraph content together and append to list
            this_article.content = " ".join(content)
            usable_articles.append(this_article)

    return usable_articles

def npr_scarper(url):
    limit = 3  # Used to limit the amount of articles to be scraped.

    # Use Requests to get content for webpage
    response = requests.get(url)

    # Use Beautiful Soup to parse HTML and find articles
    soup = BeautifulSoup(response.content, 'html5lib')
    articles = soup.find('div', class_="list-overflow").find_all('div', class_="item-info")
    
    # Store the title, link, and contents of each article in a list
    usable_articles = []
    for index, article in zip(range(limit), articles):
        this_article = Article()

        # Get article title
        this_article.title = article.find('h2').get_text()
        
        # Get article link
        this_article.link = article.find('h2').find('a')['href']
    
        # Get paragraphs from the article that are related to the article story
        response = requests.get(this_article.link)
        soup = BeautifulSoup(response.content, 'html5lib')
        paragraphs = soup.find('div', class_="storytext storylocation linkLocation").find_all('p')
        
        # Get content from each div
        content = []
        for paragraph in paragraphs:
            content.append(paragraph.get_text())

        # Join all paragraphs content together
        this_article.content = " ".join(content)
        usable_articles.append(this_article)
    
    return usable_articles

def get_articles(key):
    
    article_links = json.loads(open('links.json').read())
    articles = []

    if key == "Politics":
        for website in article_links[key]:
            articles += scrape(website['url'], website['source'])
    elif key == "Entertainment":
        for website in article_links[key]:
            articles += scrape(website['url'], website['source'])
    elif key == "Sports":
        for website in article_links[key]:
            articles += scrape(website['url'], website['source'])
    elif key == "Tech":
        for website in article_links[key]:
            articles += scrape(website['url'], website['source'])
    elif key == "Business":
        for website in article_links[key]:
            articles += scrape(website['url'], website['source'])

    return articles

def scrape(link, source):
    articles = []
    if source == "huffpost":
        articles += huffpost_scraper(link)
    elif source == "nytimes":
        articles += nytimes_scraper(link)
    elif source == "apnews":
        articles += apnews_scraper(link)
    elif source == "npr":
        articles += npr_scarper(link)
    return articles