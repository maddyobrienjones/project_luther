import pandas as pd
import datetime as dt
import re

df = pd.read_csv('imdb.csv', encoding='ISO-8859-1')

supp = pd.read_csv('money_df.csv', encoding='ISO-8859-1')
#making corresponding column names the same
supp.rename(columns={'Release Date': 'release_date', 'Movie': 'title', 'Production Budget': 'budget','Domestic Gross': 'usa_gross', 'Worldwide Gross': 'cum_ww_gross'}, inplace=True)

#converting to datetime, making year column
df['release_date'] = pd.to_datetime(df['release_date'])
df['year'] = df['release_date'].dt.year
supp['release_date'] = pd.to_datetime(supp['release_date'])
supp['year'] = supp['release_date'].dt.year

#cleaning supp as values are in str format with $s and ,s
def clean_money(val):
    val = val.replace('$', '')
    val = val.replace(',', '')
    val = int(val)
supp['budget'] = supp['budget'].apply(clean_money)
supp['usa_gross'] = supp['usa_gross'].apply(clean_money)
supp['cum_ww_gross'] = supp['cum_ww_gross'].apply(clean_money)

#dropping index columns
df.drop('Unnamed: 0', axis=1, inplace=True)
supp.drop('Unnamed: 0', axis=1, inplace=True)

#setting index to title
df.set_index('title', inplace=True)
supp.set_index('title', inplace=True)

#converting to numeric or dropping values
for each in ['budget', 'cum_ww_gross', 'ratings_count', 'runtime', 'usa_gross', 'user_rating']:
    df[each] = pd.to_numeric(df[each], errors='coerce')

#filling empty cells if in supp
df = df.combine_first(supp)

#getting rid of records with blank cells
df = df[df['country'].notnull()]
df = df[df['cum_ww_gross'].notnull()]
df= df[df['usa_gross'].notnull()]
df = df[df['budget'].notnull()]

#dropping language because only 39 records do not have English as language
df.drop('language', axis=1, inplace=True)

#~~~~~ not needed as language dropped
#changing weird language values
#df.at['The Family', 'language'] = 'English'
#df.at['Rendition', 'language'] = 'English'
#df.at['Identity Thief', 'language'] = 'English'

#language = pd.get_dummies(df['language'])
#~~~~~

#standardizing ratings
df['mpaa_rating'] = df['mpaa_rating'].fillna(value='Not Rated')
unrated_mask = (df.mpaa_rating == 'Passed') | (df.mpaa_rating == 'Approved') | (df.mpaa_rating == 'Unrated')
pg_mask = df.mpaa_rating == 'GP'
df.loc[unrated_mask,'mpaa_rating'] = 'Not Rated'
df.loc[pg_mask,'mpaa_rating'] = 'PG'

#vc = df.apply(lambda x: x.map(x.value_counts()))
#df = df.where(vc>=10, "other")

vc = df.apply(lambda x: x.map(x.value_counts()))
vc_bool = vc<10

#need to change countries that appear less than 10 times to other
df.loc[vc_bool['country'],'country']='other_country'

#need to change directors that appear less than 10 times to other
df.loc[vc_bool['director'],'director'] = 'other_director'

#combining genres to make dummy variables that can have multiple values per row
df['genre_2'] = df['genre_2'].fillna(value='None')
df['genre_3'] = df['genre_3'].fillna(value='None')
df['genres'] = df['genre_1'] + '*' + df['genre_2'] + '*' + df['genre_3']

#generating dummies
genres = df['genres'].str.get_dummies(sep='*')
country = pd.get_dummies(df['country'])
rating = pd.get_dummies(df['mpaa_rating'])
director = pd.get_dummies(df['director'])

#adding dummy variables to df
df = pd.concat([df, country, rating, director, genres], axis=1)

#dropping None genre dummy variable as meaningless
df.drop('None', axis=1, inplace=True)

#dropping categorical variables that have been replaced by dummies
df.drop(['release_date', 'country', 'director', 'genre_1', 'genre_2', 'genre_3', 'mpaa_rating', 'url', 'genres'], axis=1, inplace=True)

#adjusting year to integer
df['year'] = df['year'].apply(int)

#adding target column
df['proportion'] = df['usa_gross']/df['cum_ww_gross']

#does not make sense for us gross to be greater than cumulative worldwide gross
df = df[df['proportion']<1]

df = df.dropna(axis=0)

print(df.columns)

df.to_csv('df.csv')
