import __test__
from sklearn.datasets import load_iris

from luma.classifier.neighbors import WeightedKNNClassifier
from luma.visual.region import DecisionRegion


iris = load_iris()
X, y = iris.data, iris.target
X = X[:, :2]

wknn = WeightedKNNClassifier()
wknn.fit(X, y)

region = DecisionRegion(estimator=wknn,
                        X=X, 
                        y=y,
                        title='Weighted KNN Classifier')

region.plot()
