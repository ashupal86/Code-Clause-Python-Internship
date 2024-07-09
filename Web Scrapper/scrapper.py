from bs4 import BeautifulSoup
import requests

# write code for ffetching news headlines from the website
def news():
    """
    returns the news headlines from the website
    :return: dictionary of news headlines
    """
    url = "https://www.hindustantimes.com/"
    response=requests.Session()
    response.headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

    }
    
    page = response.get(url)
    if page.status_code!=200:
        print("failed to fetch the page")
        
    soup = BeautifulSoup(page.content, 'html.parser')
    headlines=soup.find_all('h3',class_='hdg3')
    news={}
    for headline in headlines:
        news[headline.get_text()]="https://www.hindustantimes.com"+headline.a['href']
    # print(news)
    return news



