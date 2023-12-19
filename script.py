import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

def extract(query, page):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
    url= f'https://duunitori.fi/tyopaikat/ammatti/{query}?sivu={page}'
    response = requests.get(url, headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    #return response.status_code #for checking if this actually is allowed (not allowed prints 403) 
    return soup

def transform(soup):
    jlinks = soup.find_all('a', class_='job-box__hover')
    jlistings = soup.find_all('div', class_='job-box__content')

    for link, listing in zip(jlinks, jlistings):
        link_href = link.get('href')
        full_link = 'https://duunitori.fi/' + link_href
        title = listing.find('h3', class_='job-box__title').text.strip().replace(',' ,' ')
        posted_element = listing.find('span', class_='job-box__job-posted')
        posted = posted_element.text.strip().replace('Julkaistu', '').strip() if posted_element else ''
        #print(f"Title: {title} - Location: {location} - Posted: {posted} - Link: https://duunitori.fi/{link_href}")

        job = {
            'Title': title,
            'Posted' : posted,
            'Link': full_link
        }
        joblist.append(job)
    return

joblist = []

for i in range(1,3):
    print(f'Getting page, {i}')
    c = extract('it-hajoittelija', 1)
    transform(c)

df = pd.DataFrame(joblist)
#df.to_csv('jobs.csv', index=False, sep= ',', quoting=csv.QUOTE_NONNUMERIC)


