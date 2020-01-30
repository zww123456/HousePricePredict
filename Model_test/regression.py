import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt

data = pd.read_csv('../DataGet/MyData/HouseData.csv',index_col=0)

col = data.columns
#print(data.corr())

X = data[col[:-1]]
y = data['price']


X_train,X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=0)

xgre=XGBRegressor(max_depth=8, learning_rate=0.07, n_estimators=500,
                  gammma=0.1,subsample=0.9,colsample_bytree=1.0, reg_alpha=1,
                  reg_lambda=1,min_child_weight=3)

#参数调优

cv_params ={'n_estimators': [100,300,500,700,900]}

optimized_GBM = GridSearchCV(estimator=xgre,param_grid=cv_params,
                             scoring='neg_mean_absolute_error',cv=5,verbose=1,n_jobs=4)

optimized_GBM.fit(X_train,y_train)

# print(optimized_GBM.best_score_)  最优得分

xgre.fit(X_train,y_train,eval_metric=['rmse','logloss'])

pre_test = xgre.predict(X_test)

y_act = list(y_test)

pre = [round(value) for value in pre_test]





