import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import chartify
from bokeh.layouts import gridplot

# NOTES: Release_year is only so accurate because of re-recordings of old songs. See: Irish folk, Debussy


# read in song data
songs = pd.read_csv("./data/library.csv", index_col = 0)

# create new columns for only release year, length of song in seconds
songs['release_year'] = pd.to_numeric(songs['Release'].str[:4])
# fix incorrect year on Star of the County Down
songs['release_year'][457] = 2010


time_s = []
for i in songs['Length']:
     time_s.append(sum(x * int(t) for x, t in zip([1, 60], reversed(i.split(":")))))
songs['time_s'] = (pd.Series(time_s)).values


# distributions of all relevant variables

cropped = songs[['release_year','BPM','Energy','Dance','Loud','Valence','Acoustic','Pop.','time_s']]

# histograms for distributions, including rounded mean
means = list(int(x) for x in round(cropped.mean(axis=0), 0))


ch1 = chartify.Chart(blank_labels=True, y_axis_type='density').axes.set_xaxis_label("Release year")
ch1.plot.kde(data_frame=cropped, values_column='release_year')
ch1.style.color_palette.reset_palette_order()
ch1.plot.histogram(data_frame=cropped, values_column='release_year', method='density')
ch1.callout.line(location=means[0], orientation='height')
ch1.callout.text(str(means[0]), x=means[0], y=0)
ch1.show()

ch2 = chartify.Chart(blank_labels=True, y_axis_type='density').axes.set_xaxis_label("Beats per minute")
ch2.plot.kde(data_frame=cropped, values_column='BPM')
ch2.style.color_palette.reset_palette_order()
ch2.plot.histogram(data_frame=cropped, values_column='BPM', method='density')
ch2.callout.line(location=means[1], orientation='height')
ch2.callout.text(str(means[1]), means[1], 0)
ch2.show()

ch3 = chartify.Chart(blank_labels=True, y_axis_type='density').axes.set_xaxis_label("Energy")
ch3.plot.kde(data_frame=cropped, values_column='Energy')
ch3.style.color_palette.reset_palette_order()
ch3.plot.histogram(data_frame=cropped, values_column='Energy', method='density')
ch3.callout.line(location=means[2], orientation='height')
ch3.callout.text(str(means[2]), means[2], 0)
ch3.show()

ch4 = chartify.Chart(blank_labels=True, y_axis_type='density').axes.set_xaxis_label("Danceability")
ch4.plot.kde(data_frame=cropped, values_column='Dance')
ch4.style.color_palette.reset_palette_order()
ch4.plot.histogram(data_frame=cropped, values_column='Dance', method='density')
ch4.callout.line(location=means[3], orientation='height')
ch4.callout.text(str(means[3]), means[3], 0)
ch4.show()

ch5 = chartify.Chart(blank_labels=True, y_axis_type='density').axes.set_xaxis_label("Loudness")
ch5.plot.kde(data_frame=cropped, values_column='Loud')
ch5.style.color_palette.reset_palette_order()
ch5.plot.histogram(data_frame=cropped, values_column='Loud', method='density')
ch5.callout.line(location=means[4], orientation='height')
ch5.callout.text(str(means[4]), means[4], 0)
ch5.show()

ch6 = chartify.Chart(blank_labels=True, y_axis_type='density').axes.set_xaxis_label("Positivity")
ch6.plot.kde(data_frame=cropped, values_column='Valence')
ch6.style.color_palette.reset_palette_order()
ch6.plot.histogram(data_frame=cropped, values_column='Valence', method='density')
ch6.callout.line(location=means[5], orientation='height')
ch6.callout.text(str(means[5]), means[5], 0)
ch6.show()

ch7 = chartify.Chart(blank_labels=True, y_axis_type='density').axes.set_xaxis_label("Acousticness")
ch7.plot.kde(data_frame=cropped, values_column='Acoustic')
ch7.style.color_palette.reset_palette_order()
ch7.plot.histogram(data_frame=cropped, values_column='Acoustic', method='density')
ch7.callout.line(location=means[6], orientation='height')
ch7.callout.text(str(means[6]), means[6], 0)
ch7.show()

ch8 = chartify.Chart(blank_labels=True, y_axis_type='density').axes.set_xaxis_label("Popularity")
ch8.plot.kde(data_frame=cropped, values_column='Pop.')
ch8.style.color_palette.reset_palette_order()
ch8.plot.histogram(data_frame=cropped, values_column='Pop.', method='density')
ch8.callout.line(location=means[7], orientation='height')
ch8.callout.text(str(means[7]), means[7], 0)
ch8.show()

ch9 = chartify.Chart(blank_labels=True, y_axis_type='density').axes.set_xaxis_label("Song length")
ch9.plot.kde(data_frame=cropped, values_column='time_s')
ch9.style.color_palette.reset_palette_order()
ch9.plot.histogram(data_frame=cropped, values_column='time_s', method='density')
ch9.callout.line(location=means[8], orientation='height')
ch9.callout.text(str(means[8]), means[8], 0)
ch9.show()

kdehistgrid = gridplot([ch1,ch2,ch3,ch4,ch5,ch6,ch7,ch8,ch9], ncols=3, toolbar_location=None)
