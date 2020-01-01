import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

"""
TODO: 1) Store links in dictionaries (Key = Website Link, Values = Number). The number will be used to determine which scraper to use.
      2) Return Titles , Links, and Contents from scrapers in a Pandas dataframe.
"""
# These links will be used later on in development
politic_links = ['https://www.huffpost.com/news/politics', 'https://www.nytimes.com/section/politics', 'https://apnews.com/apf-politics', 'https://www.npr.org/sections/politics/']
entertainment_links = ['https://www.huffpost.com/entertainment/', 'https://apnews.com/apf-entertainment']
sport_links = ['https://www.nytimes.com/section/sports', 'https://apnews.com/apf-sports'] 
tech_links= ['https://www.nytimes.com/section/technology', 'https://apnews.com/apf-technology', 'https://www.npr.org/sections/technology/', 'https://www.reuters.com/news/technology']
business_links = ['https://www.nytimes.com/section/business', 'https://apnews.com/apf-business', 'https://www.npr.org/sections/business/']

def nytimes_scraper(url):
    limit = 5  # Used to limit the amount of articles to be scraped

    # Use Requests to get content from webpage
    website_domain = 'https://www.nytimes.com'
    response = requests.get(url)

    # Use Beautiful Soup to parse HTML and find articles
    soup = BeautifulSoup(response.content, 'html5lib')
    articles = soup.find_all('div', class_='css-1l4spti')

    # Store the title, link, and contents of each article in a list
    titles = []
    contents = []
    links = []
    for index, article in zip(range(limit), articles):
        # Get article title
        title = article.find('h2').get_text()
        titles.append(title)

        # Get article link
        link = website_domain + article.find('a')['href']
        links.append(link)

        # Get divisions (div's) from the article that are related to the article story.
        response = requests.get(link)
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
        content_from_each_div = " ".join(content_from_each_div)
        contents.append(content_from_each_div)

    return titles, links, contents

def huffpost_scraper(url):
    limit = 5  # Used to limit the amount of articles to be scraped.
    
    # Use Requests to get content for webpage
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}  # This page will reject GET requests that do not identify a User-Agent.
    response = requests.get(url, headers=headers)

    # Use Beautiful Soup to parse HTML and find articles
    soup = BeautifulSoup(response.content, 'html5lib')
    articles = soup.find_all('div', class_='zone__content')[2].find_all('div', class_="card")
    
    # Store the title, link, and contents of each article in a list
    titles = []
    links = []
    contents = []
    for index, article in zip(range(limit), articles):
        if article.find('h2') == None:
            continue
        else:
            # Get article title
            title = article.find('h2').get_text()
            titles.append(title)

            # Get article link
            link = article.find('a')['href']
            links.append(link)

            # Get divisions (div's) from the article that are related to the article story.
            response = requests.get(link, headers=headers)
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
            content = " ".join(content)
            contents.append(content)

    return titles, links, contents

def apnews_scraper(url):
    limit = 10  # Will not find articles equal to the limit due to inconsistent HTML.
    website_domain = 'https://apnews.com'

    # Use Requests to get content for webpage
    response = requests.get(url)

    # Use Beautiful Soup to parse HTML and find articles
    soup = BeautifulSoup(response.content, 'html5lib')
    articles = soup.find_all('article', class_='feed')[0].find_all('a')  # Class names on this site is inconsistent, find all hyperlinks.

    # Store the title, link, and contents of each article in a list
    titles = []
    links = [] 
    contents = []
    for index, article in zip(range(limit), articles):
        # If the hypelink element contains a h1 element it is a link to an article.
        if article.find('h1') == None:
            continue
        else:
            # Get article title
            title = article.find('h1').get_text()
            titles.append(title)

            # Get article link
            link = website_domain + article['href']
            links.append(link)

            # Get paragraphs from the article that are related to the article story.
            response = requests.get(link)
            soup = BeautifulSoup(response.content, 'html5lib')
            paragraphs = soup.find_all('p')

            # Get content from each paragraph
            content = []
            for paragraph in paragraphs:
                content.append(paragraph.get_text())

            # Join all paragraph content together and append to list
            content = " ".join(content)
            contents.append(content)

    return titles, links, contents

def npr_scarper(url):
    limit = 5  # Used to limit the amount of articles to be scraped.

    # Use Requests to get content for webpage
    response = requests.get(url)

    # Use Beautiful Soup to parse HTML and find articles
    soup = BeautifulSoup(response.content, 'html5lib')
    articles = soup.find('div', class_="list-overflow").find_all('div', class_="item-info")
    
    # Store the title, link, and contents of each article in a list
    titles = []
    links = []
    contents = []
    for index, article in zip(range(limit), articles):
        # Get article title
        title = article.find('h2').get_text()
        titles.append(title)

        # Get article link
        link = article.find('h2').find('a')['href']
        links.append(link)

        # Get paragraphs from the article that are related to the article story
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html5lib')
        paragraphs = soup.find('div', class_="storytext storylocation linkLocation").find_all('p')
        
        # Get content from each div
        content = []
        for paragraph in paragraphs:
            content.append(paragraph.get_text())

        # Join all paragraphs content together
        content = " ".join(content)
        contents.append(content)
    
    return titles, links, contents

def huff_tester():
    titles, links, contents = huffpost_scraper('https://www.huffpost.com/news/politics')

    for i in range(0, len(titles)):
        sentiment = TextBlob(contents[i]).sentiment
        print("Title: {} \n\nLink: {} \n\nSentiment: Polarity = {}, Subjectivity = {}\n\n{}".format(titles[i], links[i], sentiment[0], sentiment[1], contents[i]))
        print("\n\n\n")

def ny_tester():
    titles, links, contents = nytimes_scraper('https://www.nytimes.com/section/politics')

    for i in range(0, len(titles)):
        sentiment = TextBlob(contents[i]).sentiment
        print("Title: {} \n\nLink: {} \n\nSentiment: Polarity = {}, Subjectivity = {}\n\n{}".format(titles[i], links[i], sentiment[0], sentiment[1], contents[i]))
        print("\n\n\n")

def ap_tester():
    titles, links, contents = apnews_scraper('https://apnews.com/apf-entertainment')

    for i in range(0, len(titles)):
        sentiment = TextBlob(contents[i]).sentiment
        print("Title: {} \n\nLink: {} \n\nSentiment: Polarity = {}, Subjectivity = {}\n\n{}".format(titles[i], links[i], sentiment[0], sentiment[1], contents[i]))
        print("\n\n\n")

def npr_tester():
    titles, links, contents = npr_scarper('https://www.npr.org/sections/business/')

    for i in range(0, len(titles)):
        sentiment = TextBlob(contents[i]).sentiment
        print("Title: {} \n\nLink: {} \n\nSentiment: Polarity = {}, Subjectivity = {}\n\n{}".format(titles[i], links[i], sentiment[0], sentiment[1], contents[i]))
        print("\n\n\n")
