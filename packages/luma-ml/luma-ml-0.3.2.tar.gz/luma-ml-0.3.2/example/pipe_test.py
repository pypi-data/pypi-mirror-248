import __test__
from luma.preprocessing.scaler import StandardScaler
from luma.reduction.linear import LDA
from luma.classifier.neighbors import WeightedKNNClassifier
from luma.visual.region import DecisionRegion
from luma.model_selection.split import TrainTestSplit
from luma.pipe.pipeline import Pipeline

from sklearn.datasets import make_blobs


X, y = make_blobs(n_samples=1000, 
                  n_features=4,
                  centers=7, 
                  cluster_std=1.0, 
                  random_state=10)

X_train, X_test, y_train, y_test = TrainTestSplit.split(X, y,
                                                        test_size=0.3,
                                                        random_state=10)

pipe = Pipeline(models=[
                    ('scaler', StandardScaler()),
                    ('lda', LDA()),
                    ('wknn', WeightedKNNClassifier())
                ],
                param_dict={
                    'lda__n_components': 2,
                    'wknn__n_neighbors': 5,
                })

pipe.fit(X_train, y_train)

plot = DecisionRegion(pipe.estimator,
                      *pipe.transform(X_test, y_test))

plot.title = 'Pipeline (StandardScaler, LDA, WKNN)'
plot.title += f'[Score: {pipe.score(X_test, y_test):.4f}]'
plot.plot()
