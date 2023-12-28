import __local__
from luma.preprocessing.imputer import SimpleImputer
from luma.preprocessing.encoder import OneHotEncoder
from luma.classifier.tree import DecisionTreeClassifier
from luma.ensemble.forest import RandomForestClassifier
from luma.model_selection.split import TrainTestSplit
from luma.model_selection.search import GridSearchCV
from luma.pipe.pipeline import Pipeline
from luma.visual.eda import CorrelationHeatMap, MissingProportion
from luma.metric.classification import Accuracy, Complex

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


train_data = pd.read_csv('example/data/spaceship/train.csv')
test_data = pd.read_csv('example/data/spaceship/test.csv')

remove_col = ['PassengerId', 'Name', 'Cabin']
train_data.drop(remove_col, axis=1, inplace=True)
test_data.drop(remove_col, axis=1, inplace=True)

train_data_np = train_data.values
test_data_np = test_data.values

X_train = train_data_np[:, :-1]
X_test = test_data_np

y_train = train_data_np[:, -1].astype(int)

pipe_pre = Pipeline(models=[
                        ('si', SimpleImputer()),
                        ('en', OneHotEncoder())
                    ],
                    param_dict={
                        'si__strategy': 'mode',
                        'en__features': [0, 2]
                    })

pipe_pre.dump()

X_train_pre = pipe_pre.fit_transform(X_train, y_train)[0]
X_test_pre = pipe_pre.fit_transform(X_test, None)[0]

X_train, X_val, y_train, y_val = TrainTestSplit.split(X_train_pre, y_train,
                                                      test_size=0.3,
                                                      random_state=10)

X_train.shape, X_val.shape
