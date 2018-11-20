#### ALL NOTES ######


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import RidgeCV, LassoCV, ElasticNet
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import train_test_split

sns.set()

def RMSE(actual, predicted):
    return np.sqrt(mean_squared_error(actual,predicted))

df = pd.read_csv('df.csv')

features = df.loc[:,['budget', 'ratings_count', 'runtime',
       'usa_gross', 'user_rating', 'year', 'Australia', 'Canada', 'China',
       'France', 'Germany', 'Hong Kong', 'Japan', 'Spain', 'UK', 'USA',
       'other_country', 'G', 'NC-17', 'Not Rated', 'PG', 'PG-13', 'R',
       'Antoine Fuqua', 'Brett Ratner', 'Chris Columbus', 'Clint Eastwood',
       'David Fincher', 'Gore Verbinski', 'Ivan Reitman', 'Joel Schumacher',
       'M. Night Shyamalan', 'Michael Bay', 'Paul W.S. Anderson',
       'Ridley Scott', 'Robert Zemeckis', 'Roland Emmerich', 'Ron Howard',
       'Steven Soderbergh', 'Steven Spielberg', 'Tim Burton', 'Tony Scott',
       'other_director', 'Action', 'Adventure', 'Animation', 'Biography',
       'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy',
       'Film-Noir', 'History', 'Horror', 'Music', 'Musical', 'Mystery',
       'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western']]

#regression results with most important coefficients next to it
poly2:
[('x22', 56410893170.02425), #R
 ('x23', 57400208779.05499), #Antoine Fuqua
 ('x7', 97335180722.3987), #Canada
 ('x12', 119338564567.8518), #Japan
 ('x33', 122657001454.85493), #Paul Anderson
 ('x20', 124959552434.52222), #PG
 ('x24', 156851795419.54974), #Brett Ratner
 ('x27', 177352154143.64835), #David Fincher
 ('x25', 206475586603.38055)] #Chris Columbus

poly3:
[('x0 x55 x62', 0.5164559124344671), #budget,horror,thriller
 ('x2 x5 x45', 0.5259398649730822), #runtime,year,animation
 ('x1^2 x47', 0.5297921490601942), #ratings_count,comedy
 ('x1 x2', 0.556184623900111), #ratings_count,runtime
 ('x0 x1 x2', 0.6006022270903557), #budget,ratings_count,runtime
 ('x1 x4 x50', 0.6383262904025876), #ratings_count,user_rating,drama
 ('x1 x5 x21', 0.673338961408061), #ratings_count,year,pg13
 ('x1 x47 x59', 0.7487205487317052), #ratings_count,comedy,romance
 ('x2 x4 x43', 0.7545912242678078)] #runtime,usa_gross,action

ridge:
[('x5 x52 x59', 0.028158423242938782), #year,fantasy,romance
 ('x3 x48 x59', 0.029220053532367108), #usa_gross,crime,romance
 ('x0^2', 0.02995333199664951), #budget
 ('x2 x4^2', 0.030384522383269084), #runtime,user_rating
 ('x3 x48 x60', 0.030565917337806506), #usa_gross,crime,scifi
 ('x2 x5', 0.03064893601012375), #runtime,year
 ('x5 x51 x59', 0.036664788591461384), #year,family,romance
 ('x1 x4 x48', 0.0376308016651948), #ratings_count,user_rating,crime
 ('x2^2 x59', 0.039216973303203714)] #runtime,romance

lasso:
[('x28^2 x48', 0.00011846288961174029), #Gore Verbinski,crime
 ('x17 x64^2', 0.00012829868244750557), #g,western
 ('x56 x57^2', 0.00014276119462426837), #music,musical
 ('x9^2 x48', 0.00016961073819779095), #france,crime
 ('x29^2 x52', 0.00020092189139530694), #Ivan Reitman,fantasy
 ('x19 x49^2', 0.00022941706097944644), #not rated,documentary
 ('x37^2 x47', 0.00023965337562426484),#Ron Howard,comedy
 ('x18^2 x62', 0.00025986100886940354), #NC17,thriller
 ('x17^3', 0.0003029060426698482)] #G

####### NOTES ##########
#Linear/Polynomial regressions
#linear regression: train: .435 vs. val: .373
#all residuals normally distributed
#all polynomials had major problems with overfitting even with ridge
#-except for lasso but R2 was very low
#poly2 unregularized: .634 vs. -1*10^25 (-10 septillion)
#poly3 unregularized: 1.0 vs. -615
#ridge poly3: .918 vs. -3.919
#lasso poly3: .19 vs. .082

#coefficients were weird

#Decision Trees
#categorical only - gbm: train: .510 vs. val: .005
#numerical + important categoricals (ww only) - gbm: .999 vs. .08
#numerical + all categoricals (ww only) - gbm: .999 vs. .118
#numericals + some categoricals (ww only)
#-gbm: .999 vs. -.015
#-rf: .899 vs. .272
#-800n,5f
#-residuals were all fairly normally distributed
#all except ww gross
#-rf: .908 vs. .379
#--RMSE: .0605 vs. .156
#--800n,5f
#-gbm: .999 vs. .362
#--.006 vs. .158
#all except usa_gross
#-rf: .899 vs. .2969
#--RMSE: .063 vs. .166
#-gbm: .999 vs. .119
#--RMSE: .005 vs. .185
#numericals minus ww
#-rf: .906 vs. .376
#-gbm: .998 vs. .245

#features were weird


###~~~Decision trees

#with both gross revenue figures (BAD)
#linear regression: train: .435 vs. val: .373
#gbm: train: .999 vs. val: .947
#gbm w some features: .999 vs. .95
#gbm w some other features: .999 vs. .953

#numerical only (BAD)
#gbm: train: .999 vs. val: .953

#categorical only
#gbm: train: .510 vs. val: .005

#important categoricals only
#gbm: train: .461 vs. val: -.039

#numerical + important categoricals (ww only)
# gbm: .999 vs. .08

#numerical + all categoricals (ww only)
# gbm: .999 vs. .118

#numericals + some categoricals (ww only)
#gbm: .999 vs. -.015
#-residuals normally distributed for train and val
#rf: .899 vs. .272
#-800n,5f
#-residuals normally distributed for train and val

#all except ww gross
#rf: .908 vs. .379
#-RMSE: .0605 vs. .156
#-800n,5f
#gbm: .999 vs. .362
#-.006 vs. .158

#all except usa_gross
#rf: .899 vs. .2969
#-RMSE: .063 vs. .166
#-residuals fairly normal
#gbm: .999 vs. .119
#-RMSE: .005 vs. .185
#-residuals fairly normal

#numericals minus ww
#rf: .906 vs. .376
#gbm: .998 vs. .245


####~~~~Polynomials
#linear regression: train: 0.266 vs. val: .184

#poly2 unregularized: .634 vs. -1*10^25 (-10 septillion)
#-train residuals normally distributed
#-val residuals are weird

#poly3 unregularized: 1.0 vs. -615
#-RMSE: .000000000000000000000004 vs. x
#-train residuals are weird
#-val residuals are mostly normal

#ridge poly3: .918 vs. -3.919
#-train residuals are normal
#-val residuals are normal
#-RMSE: 0.056 vs. 0.438

#lasso poly3: .19 vs. .082
#-train residuals normal
#-val residuals normal
#-RMSE: .178 vs. .189

