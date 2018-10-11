import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import csv
import json
import pickle

with open('codes.pkl', 'rb') as f:
    codes = pickle.load(f)

movie_links = ['https://www.imdb.com/title/'+x for x in codes]

def extract_info(url):
    response = requests.get(url)
    if response.status_code==200:
        page = response.text
        soup = BeautifulSoup(page, 'lxml')

        info = soup.find('script', attrs={'type':'application/ld+json'}).text
        info = json.loads(info)

        try:
            title = info['name']
        except:
            try:
                title = soup.find('title').text.split('(')[0].strip()
            except:
                title = None

        try:
            rating = info['aggregateRating']['ratingValue']
        except:
            try:
                rating = soup.find('span', attrs={'itemprop':'ratingValue'}).text
            except:
                rating = None

        try:
            reviewcount = info['aggregateRating']['ratingCount']
        except:
            try:
                reviewcount = soup.find('span', attrs={'class':'small', 'itemprop':'ratingCount'}).text
                reviewcount = int(reviewcount.replace(',', ''))
            except:
                reviewcount = None

        try:
            director = info['director']['name']
        except:
            try:
                if type(info['director'])==list:
                    director = list()
                    for each in info['director']:
                        director.append(each['name'])
                    director = ', '.join(director)
                else:
                    pass
            except:
                try:
                    director = soup.find(text=re.compile('Director:')).findNext().text
                except:
                    director = None

        try:
            mpaa= info['contentRating']
        except:
            mpaa = None

        try:
            if info['genre']:
                genres = info['genre']
                if type(genres)==list:
                    genre1 = genres[0]
                    genre2 = genres[1]
                    if len(genres)>2:
                        genre3 = genres[2]
                    else:
                        genre3 = None
                else:
                    genre1 = genres
                    genre2 = None
                    genre3 = None
        except:
            genre1 = None
            genre2 = None
            genre3 = None

        try:
            releasedate = soup.find('a', attrs={'title':'See more release dates'}).text.split('(')[0].strip()
            releasedate = pd.to_datetime(releasedate)
        except:
            releasedate = None

        try:
            runtime = soup.find(text=re.compile('Runtime:')).findNext().text.split()[0]
            runtime = int(runtime)
        except:
            try:
                runtime = info['duration']
                runtime = re.findall(r'\d+', runtime)
                runtime = int(runtime[0])*60 + int(runtime[1])
            except:
                runtime = None

        try:
            language = soup.find(text=re.compile('Language:')).findNext().text
        except:
            language = None

        try:
            country = soup.find(text=re.compile('Country:')).findNext().text
        except:
            country = None

        try:
            budget = soup.find(text=re.compile('Budget:')).parent.parent.text
            try:
                budget = str(budget).split('$')[1].split('(')[0].replace(',','')
                budget = int(budget)
            except:
                pass
        except:
            budget = None

        try:
            cumwwgross = soup.find(text=re.compile('Cumulative Worldwide Gross:')).parent.parent.text
            try:
                cumwwgross = str(cumwwgross).split('$')[1].replace(',','').split()[0]
                cumwwgross = int(cumwwgross)
            except:
                pass
        except:
            cumwwgross = None

        try:
            grossusa = soup.find(text=re.compile('Gross USA:')).parent.parent.text
            try:
                grossusa = str(grossusa).split('$')[1].replace(',','').split()[0]
                grossusa = int(grossusa)
            except:
                pass
        except:
            grossusa = None

        movie = {
        'title': title,
        'user_rating': rating,
        'ratings_count': reviewcount,
        'director': director,
        'mpaa_rating': mpaa,
        'genre_1': genre1,
        'genre_2': genre2,
        'genre_3': genre3,
        'release_date': releasedate,
        'runtime': runtime,
        'language': language,
        'country': country,
        'budget': budget,
        'cum_ww_gross': cumwwgross,
        'usa_gross': grossusa,
        'url': url
        }
        return movie

    else:
        return response.status_code

lod = []

for each in movie_links:
    row = extract_info(each)
    lod.append(row)

df = pd.DataFrame(lod)

with open('imdb.pkl', 'wb') as picklefile:
    pickle.dump(df, picklefile)

df.to_csv('imdb.csv')
