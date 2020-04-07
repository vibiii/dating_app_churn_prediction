# Creation of a machine learning model in order to predict the churn of a dating application

## Context / purpose
I performed this project for a dating application that wanted to be able to predict the churn of their users.
The objective for the team was to use my work to take actions in order to try to prevent their users at risk from churning.

## Data collection
The data collected by the app (client and server) is stored on a AWS Redshift that is connected to Looker (BI Platform).
I have been granted an access to Looker where I could run some sql queries on the various tables of the app's database.
Below is the process followed in order to collect the data ncessary for the project :
* Client : discussion in order to have a clear understanding of the app mechanisms and a first vision of the data that might be useful for the purpose of the project
* Looker : 
** investigation of the differents tables (around 40) in order to localize the data that need to be collected
** retrieving of the data thanks to sql queries
** saving of the data into csv files
* Python : data cleaning, exploration and usage




