import requests
from bs4 import BeautifulSoup
import pandas as pd

dictlist = []

def scraper(url):
    response = requests.get(url)
    #if working, proceed
    if response.status_code == 200:
        page = response.text
        soup = BeautifulSoup(page, 'lxml')
        #data formatted in table --> find table rows
        for tr in soup.find_all('tr'):
            moviedict = dict()
            tds = list(tr.find_all('td'))
            # all table rows formatted in same way
            if len(tds) != 0:
                moviedict['release_date'] = tds[1].text
                moviedict['title'] = tds[2].text
                moviedict['budget'] = tds[3].text
                moviedict['usa_gross'] = tds[4].text
                moviedict['cum_ww_gross'] = tds[5].text
                dictlist.append(moviedict)
            else:
                pass
    else:
        return response.status_code

#runs scraper for each page, all URLs formatted the same way
i=1
while i < 5601:
    scraper('https://www.the-numbers.com/movie/budgets/all/'+str(i))
    i += 100

#turns list of dicts returned by scraper into dataframe
money_df = pd.DataFrame(dictlist)

money_df.to_csv('money_df.csv')
