from sklearn.decomposition import PCA
from sklearn import svm
import matplotlib.pyplot as plt
import numpy as np
from bokeh.plotting import figure, show, output_file, save
from bokeh.models import value, LabelSet, ColumnDataSource
output_file("./spotify_pca.html", title = "spotify pca")

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

# PCA to zoomable plot

source = ColumnDataSource(dict(
    x = x_pca[:,0],
    y = x_pca[:,1],
    titles = songs['Title']
))


p = figure(plot_width = 1500, plot_height = 800, tools = "pan,wheel_zoom,box_zoom,reset,previewsave",
           x_axis_type = None, y_axis_type = None, min_border=1)

p.scatter(x='x',y='y', source=source)

labels = LabelSet(x='x',y='y',text='titles',level='glyph',
              x_offset=5, y_offset=5, source=source, render_mode='canvas', text_font_size='8pt', text_alpha=0.7)

p.add_layout(labels)

show(p)


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
# dense cluster toward the bottom is a mashup of 90s pop, indie, and alternative favorites -- perfect suggestion area!