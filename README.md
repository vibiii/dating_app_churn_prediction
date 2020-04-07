# Creation of a machine learning model in order to predict the churn of a dating application

## Context / purpose
I performed this project for a dating application that wanted to be able to predict the churn of their users.
The objective for the team was to use my work to take actions in order to try to prevent their users at risk from churning.

Churn here is defined as 'early churn' meaning new users that are leaving the app very quickly.
My final objective is to predict the users that are not going to show up in week 2 according to their inapp experience during the 5 first days. 

## Files description
This repository is composed of the following folders :
* 2_Visualization composed of :
 * visualization.ipynb : jupyter notebook including the code for the visualization part of the project
 * some png images that are presented below in this README
* 3_Models composed of  :
 * men_churn_model.ipynb and women_churn_model.ipynb : the jupyter notebook including the code for the modeling part of the project
 * some png images that are presented below in this README
* 4_Models_operation composed of the python script (Churn_prediction_script.py) that will be used in order to apply the models to the new data
* churn_predicion_presentation : a pdf presentation that summarizes the project and gives a more complete view of the process I followed.

## Data collection
The data collected by the app (client and server) is stored on a AWS Redshift that is connected to Looker (BI Platform).
I have been granted an access to Looker where I could run some sql queries on the various tables of the app's database.
Below is the process followed in order to collect the data necessary for the project :
* Client : discussion in order to have a clear understanding of the app mechanisms and a first vision of the data that might be useful for the purpose of the project
* Looker : 
  * investigation of the differents tables (around 40) in order to localize the data that need to be collected
  * retrieving of the data thanks to sql queries
  * saving of the data into csv files
* Python : data cleaning, exploration and usage

I collected the data of all the new users during a 2 months period (120k people)

The data collected can be classified in several categories :
* personal information :
 * gender
 * age
 * country
 * platform (iOS, Android, web)
* user behaviour in the application during the 5 first days :
 * Logins : number of days when the users logged-in to the app
 * Connections : number of connections with other user the users got (meaning both users "liked" each other)
 * Chat request sent / received
 * Purchases : in-app purchases made by the users
 * Virtual currency spending : virtual currency can be acquired (or bought) in the application and can be used in different ways like sending chat requests, getting additional mathches, etc...
 * Number of ratings given : user can see different profiles of other users and give thel a rating
 * Average rating given
* other :
 * Acquisition mean (paid/organic) : if the user downloaded the application through organic research or if he was brought through a marketing campaign
 * Number of ratings received
 * Average rating received
 
## Data cleaning
In python I imported the various csv resulting from the sql queries and merged them into a dataframe.
The cleaning mainly consisted in filling the missing values by 0 due to the sql queries results.
I created several new columns in order to get more synthetic information (mainly for visualization purpose) :
* number of logins during the first 5 days
* total spent in in app purchases
* total virtual currency spent
* user has spent virtual currency (Y/N)
* user got at least a connection (Y/N)

I cleaned the countries in order to get a limited number of categories
I removed from the data the users that have been detected as fraud by the team (I was provided with a csv list of those users) and that could bias my analysis.

## Exploration and visualization

The data exploration and visualization has been done using the matplotlib and seaborn librairies.
It has highlighted some key information that affected my methodology for this project :
* the gender repartition of the user base is imbalanced : fewer women are installing the app and they tend to churn more easiy than men 
![picture alt](https://github.com/vibiii/dating_app_churn_prediction/blob/master/2_Visualization/01_Gender_repartition.png)
![picture alt](https://github.com/vibiii/dating_app_churn_prediction/blob/master/2_Visualization/05_Gender_proba_stay.png)
* some user behaviour tend to clearly hae an impact on the churn of users mainly :
 * the fact that the users got a connection in the first days
![picture alt](https://github.com/vibiii/dating_app_churn_prediction/blob/master/2_Visualization/Connection_churn_men.png)
![picture alt](https://github.com/vibiii/dating_app_churn_prediction/blob/master/2_Visualization/Connection_churn_women.png)
 * the number of logins during the first days
 * the spending behaviour
 * the virtual currency spending behaviour
 
 All the visualization are available in the pdf file 'churn_predicion_presentation'
 
 Due to the fact that the genre repartition of the user base is imbalanced, the 'rules' applied by the app to both genders are not the same.
 For example :
 * lots of features are free for women while men have to spend virtual currency for using them
 * the number of daily matches is not the same for men and women
 
 **As a consequence I have decided to build 2 DIFFERENT MODELS in order to predict the churn of men and women**
 
 ## Data processing
 
 In order to apply predictive model I modified the data collected to make it more usable. 
 The main modifications performed are :
 * Transformation of categorical data into dummies
 * Winsorize of the ratings and chat requests columns in order to remove outliers
 * Standardization of numerical columns
 
 ## Models 
 
 Below are the various process steps conducted for both men and women
 ![picture alt](https://github.com/vibiii/dating_app_churn_prediction/blob/master/3_Models/Process_steps.JPG)
 
 
 In order to easily run the various models, I created a function that :
 * takes as input :
  * the model
  * the training and testing set
 * prints :
  * the model clasification report 
  * the following scores : accuracy, precision, recall
  * the confusion matrix
  * the roc curve
  * the features importance for the models that have it
 ![picture alt](https://github.com/vibiii/dating_app_churn_prediction/blob/master/3_Models/Model_func.JPG)
 
 Below is the result of the function for the logistic regression 
  ![picture alt](https://github.com/vibiii/dating_app_churn_prediction/blob/master/3_Models/Logit.JPG)
  
 Since I want to minimize the false negative, the performance of the model was assessed based on the recall score (as close as possible to 100%) without precision being too bad.
 
 After determining the 2 best models for each genre:
 * I tunned their hyper parameters to improve them again
 * Ensemble them into 2 final models (men / women)
 * Pickled the final models in order to be able to re_use them
 
 The result of the final models are :
 * Men :
  * Precision : 82%
  * False negative rate : 21%
 * Women :
  * Precision : 83%
  * False negative rate : 21%
 
 ## Deliverable to the client
 
 I provided my client with the following files in order for him to use my model on a daily basis :
 * The sql queries that will allow to collect the data requested by the model (they are much lighter than the initial queries because thanks to the feature engineering I have reduced the number of variables needed)
 * A python script (Churn_prediction_script.py located in 4_Models_operation) that will :
  * collect all the csv files located in the same folder (this way it requires less processing from the client, he only has to save the csv files resulting from the queries in the same folder as the python script without having to modify any path in the script)
  * apply the models to the data provided by the csv files
  * export a csv file (in the same folder), containing the list of the users that are considered as liable to churn.
  
## Built with

* Python - The programming language used
* Pandas - library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming language
* MySQL - MySQL is an open-source relational database management system for SQL
* Looker - Popular Data visualization tool
* MatPlotLib - Matplotlib is a Python 2D plotting library which produces publication quality figures in a variety of hardcopy formats and interactive environments across platforms
* Seaborn - Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics
* Scikit-learn - Scikit-learn is a machine learning library for Python

 





