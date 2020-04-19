# ipl-reactive-dashboard

Basic reactive-dashboard based on [IPL Dataset](https://www.kaggle.com/nowke9/ipldata) from Kaggle, deployed on Heroku. 

The [dataset](https://www.kaggle.com/nowke9/ipldata) is stored on the author's Google Drive - retrieved using the Google Drive API Client. 

[Streamlit](https://www.streamlit.io/) has been used to create an interactive data-app(converting the Jupyter-notebook based EDA/visualization into a reactive app)

## How to run: 

The Heroku deployment of the dashboard is hosted at: https://fierce-woodland-33825.herokuapp.com/



## Notes: 

1. **Source files and their relevance**: 

   preprocess.py: defines functions for pre-processing data as well as for visualizations displayed in app.py

   tables.py: creates tables for visualizations using functions in preprocess.py 

   connect_to_google_drive.py - Authenticates credentials, connects to Google Drive API and retrieves the data file from owner's personal drive. 


2. notebooks - contains the Jupyter Notebook .ipynb files - where I performed EDA and Visualization(in a not-so-neat manner). 
Does not render graphs in github. [Can be viewed here](https://github.com/chettriyuvraj/ipl-reactive-dashboard/blob/master/notebooks/IPL%20-%20EDA%20and%20Visualization.ipynb)


3. The repository contains a folder 'dummycredentials'. In the actual implementation - this is a folder named 'credentials' which contains 
the key for connecting to the Google Drive API(reflected in code file - connect_to_google_drive.py)


4. If you want to self-deploy - changes will have to be made accordingly @ connect_to_google_drive.py


5. All undocumented files such as 'Procfiles', 'procGen.py', et al are pre-requisites for the Heroku Deployment - they have been explained in the references provided below.



## References: 

1. [Deploying streamlit dashboard on Heroku](https://gilberttanner.com/blog/deploying-your-streamlit-dashboard-with-heroku)
2. [Google Drive API](https://developers.google.com/drive)
3. [Connect and download files from Google Drive API](https://medium.com/@umdfirecoml/a-step-by-step-guide-on-how-to-download-your-google-drive-data-to-your-jupyter-notebook-using-the-52f4ce63c66c)


