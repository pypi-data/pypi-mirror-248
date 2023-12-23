from luma.migrate.port import ModelPorter

from sklearn.datasets import load_digits
import matplotlib.pyplot as plt


X, y = load_digits(return_X_y=True)


port = ModelPorter()
tsne = port.load(filepath='example/model/digits_tsne.luma')

X = tsne.transform()

plt.scatter(X[:, 0], X[:, 1], c=y, cmap='rainbow')
plt.tight_layout()
plt.show()
