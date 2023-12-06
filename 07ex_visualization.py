# -*- coding: utf-8 -*-
"""07ex_visualization.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oVH3WB8YPiAvImujVoZ9WXhDZ_ca8Cxe

1\. **Spotting correlations**

Load the remote file:

```bash
https://www.dropbox.com/s/aamg1apjhclecka/regression_generated.csv
```

with Pandas and create scatter plots with all possible combinations of the following features:
    
  + `features_1`
  + `features_2`
  + `features_3`
  
Are these features correlated? Please add a comment.
"""

!wget https://www.dropbox.com/s/aamg1apjhclecka/regression_generated.csv

import pandas as pd
df = pd.read_csv('/content/regression_generated.csv')
df

import matplotlib.pyplot as plt
from itertools import combinations

features = df.columns[1:4]

combinations_of_features = list(combinations(features, 2))

num_cols = len(combinations_of_features)
fig, axes = plt.subplots(1, num_cols, figsize=(15, 5))

for i, combination in enumerate(combinations_of_features):
    col = i % num_cols
    axes[col].scatter(df[combination[0]], df[combination[1]], c=df['label'], cmap='plasma')
    axes[col].set_xlabel(combination[0])
    axes[col].set_ylabel(combination[1])
    axes[col].set_title(f'Scatter Plot for {combination[0]} vs {combination[1]}')

# Adjust layout
plt.tight_layout()
plt.show()

"""2\. **Color-coded scatter plot**

Produce a scatter plot from a dataset with two categories.

* Write a function that generates a 2D dataset consisting of 2 categories. Each category should distribute as a 2D gaussian with a given mean and standard deviation. Set different values of the mean and standard deviation between the two samples.
* Display the dataset in a scatter plot marking the two categories with different marker colors.

An example is given below:
"""

from IPython.display import Image
Image('images/two_categories_scatter_plot.png')

import numpy as np
def generate2dDataset():
  firstSample = np.random.multivariate_normal([2, 2],1*np.eye(2) , 100)
  secondSample = np.random.multivariate_normal( [-2, -2],1.5*np.eye(2) , 100)
  dataset = np.vstack([firstSample, secondSample])
  labels = np.concatenate([ np.array([0] * 100),np.array([1] * 100)])
  return dataset, labels

dataset, labels = generate2dDataset()
plt.scatter(dataset[labels == 0, 0], dataset[labels == 0, 1], label='Category 0',color='red', alpha=0.7)
plt.scatter(dataset[labels == 1, 0], dataset[labels == 1, 1], label='Category 1', alpha=0.7)

# Set labels and title
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('Scatter Plot of 2D Gaussian Dataset')
plt.show

"""3\. **Profile plot**

Produce a profile plot from a scatter plot.
* Download the following pickle file:
```bash
wget https://www.dropbox.com/s/3uqleyc3wyz52tr/residuals_261.pkl -P data/
```
* Inspect the dataset, you'll find two variables (features)
* Convert the content to a Pandas Dataframe
* Clean the sample by selecting the entries (rows) with the absolute values of the variable "residual" smaller than 2
* Plot a Seaborn `jointplot` of "residuals" versus "distances", and use seaborn to display a linear regression.

Comment on the correlation between these variables.

* Create manually (without using seaborn) the profile histogram for the "distance" variable; choose an appropriate binning.
* Obtain 3 numpy arrays:
  * `x`, the array of bin centers of the profile histogram of the "distance" variable
  * `y`, the mean values of the "residuals", estimated in slices (bins) of "distance"
  * `err_y`, the standard deviation of the of the "residuals", estimated in slices (bins) of "distance"
* Plot the profile plot on top of the scatter plot
"""

!wget https://www.dropbox.com/s/3uqleyc3wyz52tr/residuals_261.pkl

import seaborn as sns

data = pd.read_pickle('/content/residuals_261.pkl')
data = pd.DataFrame(data.tolist())

cleaned_data = data[np.abs(data['residuals']) < 2]
sns.jointplot(x='distances', y='residuals', data=cleaned_data, color='blue',alpha=0.6)
sns.regplot(x='distances', y='residuals', data=cleaned_data, scatter=False, color='orange')

correlation = cleaned_data['distances'].corr(cleaned_data['residuals'])
print(f"Correlation between 'distances' and 'residuals': {correlation}")

num_bins = 20
bins = np.linspace(cleaned_data['distances'].min(), cleaned_data['distances'].max(), num_bins + 1)

x = (bins[:-1] + bins[1:]) / 2
y = []
err_y = []

for i in range(num_bins):
    bin_mask = (cleaned_data['distances'] >= bins[i]) & (cleaned_data['distances'] < bins[i + 1])
    residuals_in_bin = cleaned_data.loc[bin_mask, 'residuals']

    y.append(np.mean(residuals_in_bin))
    err_y.append(np.std(residuals_in_bin))

x = np.array(x)
y = np.array(y)
err_y = np.array(err_y)

plt.figure(figsize=(10, 6))

sns.scatterplot(x='distances', y='residuals', data=cleaned_data, alpha=0.7)

plt.errorbar(x, y, yerr=err_y, fmt='o-', color='red', label='Profile Plot')

plt.xlabel('Distances')
plt.ylabel('Residuals')
plt.title('Profile Plot with Scatter Plot')


plt.legend()
plt.show()

"""##**Comment About Correlation of 2 features:**

Correlation between 'distances' and 'residuals' ~= **0.043**

The positive sign indicates that as the 'distances' variable increases, the 'residuals' variable tends to increase slightly. However, the strength of this relationship is weak.

4\. **Kernel Density Estimate**

Produce a KDE for a given distribution (by hand, not using seaborn):

* Fill a numpy array `x` of length N (with $N=\mathcal{O}(100)$) with a variable normally distributed, with a given mean and standard deviation
* Fill an histogram in pyplot taking proper care of the aesthetic:
   * use a meaningful number of bins
   * set a proper y axis label
   * set proper value of y axis major ticks labels (e.g. you want to display only integer labels)
   * display the histograms as data points with errors (the error being the poisson uncertainty)
* For every element of `x`, create a gaussian with the mean corresponding to the element value and the standard deviation as a parameter that can be tuned. The standard deviation default value should be:
$$ 1.06 * x.std() * x.size ^{-\frac{1}{5}} $$
you can use the scipy function `stats.norm()` for that.
* In a separate plot (to be placed beside the original histogram), plot all the gaussian functions so obtained
* Sum (with `np.sum()`) all the gaussian functions and normalize the result such that the integral matches the integral of the original histogram. For that you could use the `scipy.integrate.trapz()` method. Superimpose the normalized sum of all gaussians to the first histogram.
"""

from scipy.stats import norm
from scipy.integrate import trapz

sample_size = 100
mean = 10
std_dev = 2

data = np.random.normal(mean, std_dev, sample_size)
hist, bin_edges = np.histogram(data, bins=20, density=False)
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
bin_width = bin_edges[1] - bin_edges[0]
poisson_errors = np.sqrt(hist)

plt.figure(figsize=(12, 6))
plt.bar(bin_centers, hist, width=bin_width, color='blue', alpha=0.7, label='Histogram with Poisson Errors')
plt.errorbar(bin_centers, hist, yerr=poisson_errors, fmt='none', ecolor='black', capsize=2)

std_dev_factor = 1.06 * data.std() * data.size**(-1/5)
gaussian_sum = np.zeros_like(bin_centers)

for xi in data:
    gauss = norm.pdf(bin_centers, loc=xi, scale=std_dev_factor * data.std())
    plt.plot(bin_centers, gauss, 'r--', alpha=0.1)
    gaussian_sum += gauss

area_hist = trapz(hist, x=bin_centers)
area_gauss_sum = trapz(gaussian_sum, x=bin_centers)
gaussian_sum_normalized = gaussian_sum * (area_hist / area_gauss_sum)
plt.plot(bin_centers, gaussian_sum_normalized, color='green', label='Normalized Sum of Gaussians')

plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Kernel Density Estimate (KDE) and Sum of Gaussians')
plt.legend()

plt.yticks(np.arange(0, max(hist) + 2, 2))
plt.show()