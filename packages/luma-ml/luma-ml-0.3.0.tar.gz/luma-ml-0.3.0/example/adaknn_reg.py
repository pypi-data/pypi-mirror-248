import __test__
from luma.regressor.neighbors import AdaptiveKNNRegressor
from luma.metric.regression import RootMeanSquaredError as rmse

from sklearn.datasets import make_regression
import matplotlib.pyplot as plt
import numpy as np


X, y = make_regression(n_features=1, n_samples=100, noise=10, random_state=0)

adaknn = AdaptiveKNNRegressor(n_density=10,
                              min_neighbors=5,
                              max_neighbors=20)

adaknn.fit(X, y)

X_test = np.linspace(-3, 3, 100).reshape(-1, 1)
y_pred = adaknn.predict(X_test)

plt.scatter(X, y, c='royalblue', marker='x', s=15, label='Train values')
plt.plot(X_test, y_pred, color='crimson', linewidth=2, label='Predicted plot')
plt.grid()
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title(f'Adaptive kNN Regression [RMSE: {adaknn.score(X, y, metric=rmse):.4f}]')
plt.tight_layout()
plt.show()
