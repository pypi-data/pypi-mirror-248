import __test__
from luma.migrate.port import ModelPorter
from luma.visual.region import DecisionRegion

from sklearn.datasets import load_digits


X, y = load_digits(return_X_y=True)

port = ModelPorter()
tsne = port.load('example/model/digits_tsne.luma')
ada = port.load('example/model/digits_adaknn.luma')

print(ada.__dict__)

X = tsne.transform()

region = DecisionRegion(estimator=ada,
                        X=X, y=y)

region.plot()
