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

###~~~Decision trees

#with both gross revenue figures
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

#numericals minus ww
#rf: .906 vs. .376
#gbm: .998 vs. .245


####~~~~Polynomials
#linear regression: train: 0.266

#poly2 unregularized: .634 vs. -1*10^25
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
