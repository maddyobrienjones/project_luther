# Welcome to my 'Project Luther' repo!   

In this project at Metis, I used web scraping with BeautifulSoup and Selenium to gather information on films from IMDB. Then, I tested linear regression and decision tree models to try and predict the proportion of revenue movies get from the USA versus the rest of the world.   

In this repo, I've uploaded my code, the data I used, and the presentation I gave at Metis on this project.  
  
Blog Post:  
  
## Here is a summary of of each document in the repo:   

### Data
* codes.csv - list of IMDB movie codes
* codes.pkl - codes.csv in pickled format for ease of use
* df.csv - cleaned data for modeling
* imdb.csv - raw IMDB data
* imdb.pkl - raw IMDB data in pickled format for ease of use
* money.csv - supplementary data on budgets and box office grosses
  
### Web Scraping and Data Cleaning
* scraper.py - scraper used to gather data from each movie
* selenium_link_scraper.py - scraper used to gather IMDB movie codes
* cleaning.py - cleaning of raw IMDB data
  
### Model Testing
* gbm_model.ipynb - building of gradient-boosting model
* model_test.ipynb - miscellaneous model testing
* poly_model.ipynb - building of polynomial model