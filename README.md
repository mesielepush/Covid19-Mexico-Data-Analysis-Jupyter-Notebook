# Covid19 Mexico Data Analysis
 Analysis for Covid19 Mexico's official patients Data

Through this [notebook](https://github.com/mesielepush/Covid19-Mexico-Data-Analysis-Jupyter-Notebook/blob/master/MexicoCovidDescriptiveGeneral.ipynb) you can explore the Covid19 official data from Mexico.
  
The notebook revolves around the Covid python class described in [Covid_suite.py](https://github.com/mesielepush/Covid19-Mexico-Data-Analysis-Jupyter-Notebook/blob/master/Covid_suite.py)

Documentation can be found in this [notebook](https://github.com/mesielepush/Covid19-Mexico-Data-Analysis-Jupyter-Notebook/blob/master/Documentation%20for%20Covid%20Class.ipynb).  

## Dependencies

For most of the notebook you just need:

* python3.6 >=
* ipython==7.13.0
* pandas==1.0.3
* numpy==1.18.1
* matplotlib==3.1.3
* joblib==0.15.1
* seaborn==0.10.1

There is an implementation of a classifier that doesn't work because there is no enough data to discriminate clearly. You can, however, run it to see the ROC curves. A quick explanation about why it doesn't work is in the [documentation](https://github.com/mesielepush/Covid19-Mexico-Data-Analysis-Jupyter-Notebook/blob/master/Documentation%20for%20Covid%20Class.ipynb).  
To run that classifier you'll need

* xgboost==0.90
* sklearn==0.0

![function photo](https://i.imgur.com/uAcop03.png)


The database updates daily from [the official page](https://coronavirus.gob.mx/datos/#DownZCSV).

<br>

![official data page](https://i.imgur.com/Z6JoKG0.png)

## Installation

To install just download or fork this repository, open jupyter notebook on the container folder and run either the [documentation notebook](https://github.com/mesielepush/Covid19-Mexico-Data-Analysis-Jupyter-Notebook/blob/master/Documentation%20for%20Covid%20Class.ipynb) or the main [explorer notebook](https://github.com/mesielepush/Covid19-Mexico-Data-Analysis-Jupyter-Notebook/blob/master/Documentation%20for%20Covid%20Class.ipynb).  