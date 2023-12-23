from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import __test__
from luma.regressor.neighbors import WeightedKNNRegressor
from luma.metric.regression import RootMeanSquaredError


np.random.seed(42)
X = np.random.uniform(-5, 5, (100, 2))
y = np.sin(X[:, 0]) + np.cos(X[:, 1])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = WeightedKNNRegressor(n_neighbors=5)
model.fit(X_train, y_train)
predictions = model.predict(X_test)

x1_range = np.linspace(X[:, 0].min() - 1, X[:, 0].max() + 1, 50)
x2_range = np.linspace(X[:, 1].min() - 1, X[:, 1].max() + 1, 50)
x1_grid, x2_grid = np.meshgrid(x1_range, x2_range)
grid = np.c_[x1_grid.ravel(), x2_grid.ravel()]

grid_predictions = model.predict(grid).reshape(x1_grid.shape)

fig = plt.figure(figsize=(5.5, 5))
ax = fig.add_subplot(1, 1, 1, projection='3d')

ax.scatter(X_train[:, 0], X_train[:, 1], y_train, 
           color='blue', 
           label='Training Data',
           alpha=0.5)
ax.scatter(X_test[:, 0], X_test[:, 1], y_test, 
           color='red', 
           label='Test Data',
           alpha=0.5)
ax.plot_surface(x1_grid, x2_grid, grid_predictions, 
                cmap='rainbow', 
                label='Predicted Surface',
                alpha=0.5)

ax.set_xlabel(r'$x_1$')
ax.set_ylabel(r'$x_2$')
ax.set_zlabel(r'$y$')
ax.legend()

plt.title(f'Weighted KNN Regressor [RMSE: {model.score(X_test, y_test, RootMeanSquaredError):.4f}]')
plt.tight_layout()
plt.show()

