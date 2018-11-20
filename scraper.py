import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
import csv
import json
import pickle

#contains all movie codes, scraped from genre pages of imdb --> urls formatted like imdb.com/title/'code'
with open('codes.pkl', 'rb') as f:
    codes = pickle.load(f)

movie_links = ['https://www.imdb.com/title/'+x for x in codes]

def extract_info(url):
    response = requests.get(url)
    #if works, proceed
    if response.status_code==200:
        page = response.text
        soup = BeautifulSoup(page, 'lxml')
        #for some pages, data stored in json format --> easier to parse
        info = soup.find('script', attrs={'type':'application/ld+json'}).text
        info = json.loads(info)
        
        #scraping data with try, except clause as many of the pages have slightly different formats
        
        try: #if json
            title = info['name']
        except: #search in html
            try:
                title = soup.find('title').text.split('(')[0].strip()
            except:
                title = None

        try: #if json
            rating = info['aggregateRating']['ratingValue']
        except: #search in html
            try:
                rating = soup.find('span', attrs={'itemprop':'ratingValue'}).text
            except:
                rating = None

        try: #if json
            reviewcount = info['aggregateRating']['ratingCount']
        except: #search in html
            try:
                reviewcount = soup.find('span', attrs={'class':'small', 'itemprop':'ratingCount'}).text
                reviewcount = int(reviewcount.replace(',', ''))
            except:
                reviewcount = None

        try: #if json
            director = info['director']['name']
        except: #search in html
            try:
                if type(info['director'])==list:
                    director = list()
                    for each in info['director']:
                        director.append(each['name'])
                    director = ', '.join(director)
                else:
                    pass
            except: #listed multiple times or in different places on some pages
                try:
                    director = soup.find(text=re.compile('Director:')).findNext().text
                except:
                    director = None

        try: #if json
            mpaa= info['contentRating']
        except:
            mpaa = None

        try: #if json
            if info['genre']: #make sure all genres are captured
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

        try: #search in html
            releasedate = soup.find('a', attrs={'title':'See more release dates'}).text.split('(')[0].strip()
            releasedate = pd.to_datetime(releasedate)
        except:
            releasedate = None

        try: #search in html
            runtime = soup.find(text=re.compile('Runtime:')).findNext().text.split()[0]
            runtime = int(runtime)
        except:
            try: #if json, does not always work correctly
                runtime = info['duration']
                runtime = re.findall(r'\d+', runtime) #formatted as 1H30M
                #need to multiply first number by 60 and add second number to get runtime as minutes
                runtime = int(runtime[0])*60 + int(runtime[1])             
            except:
                runtime = None

        try: #search in html
            language = soup.find(text=re.compile('Language:')).findNext().text
        except:
            language = None

        try: #search in html
            country = soup.find(text=re.compile('Country:')).findNext().text
        except:
            country = None

        try: #search in html
            budget = soup.find(text=re.compile('Budget:')).parent.parent.text
            try: #parsing out number
                budget = str(budget).split('$')[1].split('(')[0].replace(',','')
                budget = int(budget)
            except:
                pass
        except:
            budget = None

        try: #search in html
            cumwwgross = soup.find(text=re.compile('Cumulative Worldwide Gross:')).parent.parent.text
            try: #clean
                cumwwgross = str(cumwwgross).split('$')[1].replace(',','').split()[0]
                cumwwgross = int(cumwwgross)
            except:
                pass
        except:
            cumwwgross = None

        try: #search in html
            grossusa = soup.find(text=re.compile('Gross USA:')).parent.parent.text
            try: #clean
                grossusa = str(grossusa).split('$')[1].replace(',','').split()[0]
                grossusa = int(grossusa)
            except:
                pass
        except:
            grossusa = None
        
        #creating dictionary for each movie to append to list
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

#creating list of dicts to turn into dataframe
for each in movie_links:
    row = extract_info(each)
    lod.append(row)

df = pd.DataFrame(lod)

with open('imdb.pkl', 'wb') as picklefile:
    pickle.dump(df, picklefile)

df.to_csv('imdb.csv')
