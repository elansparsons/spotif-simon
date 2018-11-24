from sklearn.decomposition import PCA
from sklearn import svm
import matplotlib.pyplot as plt
import numpy as np

# find PCA shape, connect to songs to see outliers
pca = PCA(n_components=2)
pca.fit(cropped)

print(pca.explained_variance_ratio_)

x_pca = pca.fit_transform(cropped)
x = x_pca[:,0]
y = x_pca[:,1]
titles = songs['Title']

plt.figure(figsize=(12,8))
plt.scatter(x, y, c='black') # x -300 450, y -75 110
for title, x, y in zip(titles, x, y):
 plt.annotate(title, xy=(x, y))
plt.show()

# One class SVM with contours to show similarity/dissimilarity/recommendations
classified = svm.OneClassSVM(kernel='rbf', gamma=0.001, nu=0.3)
classified.fit(x_pca)

xx, yy = np.meshgrid(np.linspace(-300,500, num=500), np.linspace(-300,500, num=500))

Z = classified.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)
plt.figure(1, figsize=(14,8),)
plt.contourf(xx, yy, Z, levels=np.linspace(Z.min(),0,7), cmap=plt.get_cmap('inferno'))
a = plt.contour(xx, yy, Z, levels=[0], linewidths=2, colors='magenta')
plt.contourf(xx, yy, Z, levels=[0, Z.max()], colors='#e25cfd')

b1 = plt.scatter(x_pca[:,0], x_pca[:,1], c='white', s = 10)
plt.axis('tight')
plt.xlim((-300,450))
plt.ylim((-125,150))
plt.show()

# outliers to the right are mostly Irish folk music and Coheed & Cambria with long song durations
# left cluster is very short durations
