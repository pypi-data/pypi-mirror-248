import __test__
from luma.model_selection.split import TrainTestSplit
from luma.preprocessing.scaler import StandardScaler
from luma.classifier.neighbors import KNNClassifier, AdaptiveKNNClassifier
from luma.classifier.logistic import SoftmaxRegressor
from luma.classifier.naive_bayes import GaussianNaiveBayes
from luma.classifier.svm import SVC, KernelSVC
from luma.classifier.tree import DecisionTreeClassifier
from luma.ensemble.forest import RandomForestClassifier

from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
import numpy as np

seed = 10

X, y = make_blobs(n_samples=500, 
                  centers=7, 
                  cluster_std=1.5, 
                  random_state=seed)

sc = StandardScaler()
X = sc.fit_transform(X)

X_train, X_test, y_train, y_test = TrainTestSplit.split(X, y, 
                                                        test_size=0.3,
                                                        random_state=seed)

models = [KNNClassifier(), AdaptiveKNNClassifier(), SoftmaxRegressor(),
          GaussianNaiveBayes(), SVC(), KernelSVC(), 
          DecisionTreeClassifier(),RandomForestClassifier()]

for model in models:
    model.fit(X_train, y_train)

x1_min, x1_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
x2_min, x2_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, 0.02),
                       np.arange(x2_min, x2_max, 0.02))

fig, axes = plt.subplots(2, 4, figsize=(16, 8))

for ax, model in zip(axes.flatten(), models):
    Z = model.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    ax.contourf(xx1, xx2, Z, alpha=0.4, cmap='rainbow')
    ax.set_xlim(xx1.min(), xx1.max())
    ax.set_ylim(xx2.min(), xx2.max())

    ax.scatter(X_train[:, 0], X_train[:, 1], 
               c=y_train, cmap='rainbow', marker='o', 
               alpha=0.8, edgecolors='black', label='Train')
    
    ax.scatter(X_test[:, 0], X_test[:, 1], 
               c=y_test, cmap='rainbow', marker='D', 
               alpha=0.8, edgecolors='black', label='Test')
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'{model.__class__.__name__} [Score: {model.score(X_test, y_test):.2f}]')
    ax.legend()

plt.tight_layout()
plt.show()
