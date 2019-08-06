catheat
=======
Wrapper for [seaborn](http://seaborn.pydata.org) to plot categorical heatmaps. Tested with seaborn version `0.8.1`.

## Installation
I recommend using [Python Packaging Index (PIP)](https://pypi.python.org/pypi) to install.
First, get [PIP](https://pip.pypa.io/en/stable/installing/) and then run in terminal:

`pip install git+git://github.com/schlegelp/catheat@master`

This command should also work to update the package.

If your default distribution is Python 2, you have to explicitly tell [PIP](https://pip.pypa.io/en/stable/installing/) to install for Python 3:

`pip3 install git+git://github.com/schlegelp/catheat@master`

If you are behind a firewall try:

`pip install git+https://github.com/schlegelp/catheat@master`

#### Dependencies:
- [seaborn](http://seaborn.pydata.org)
- [Pandas](http://pandas.pydata.org/)
- [Numpy](http://www.scipy.org)
- [Matplotlib](http://www.matplotlib.org)

## Quickstart:

### Plot a simple categorical heatmap
```python
import catheat
import seaborn as sns

# Get an example dataset from seaborn
tips = sns.load_dataset('tips')

# Plot the categorical columns as heatmap
ax = catheat.heatmap(tips[['sex','smoker','day','time','size']],
                     palette='Paired')

plt.show()

```

<img src="https://user-images.githubusercontent.com/7161148/34643797-af6b040a-f322-11e7-98ad-db562cfa9951.png" width="650">

## License:
This code is under GNU GPL V3
