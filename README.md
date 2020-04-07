# Creation of a machine learning model in order to predict the churn of a dating application

## Context / purpose
I performed this project for a dating application that wanted to be able to predict the churn of their users.
The objective for the team was to use my work to take actions in order to try to prevent their users at risk from churning.

Churn here is defined as 'early churn' meaning new users that are leaving the app very quickly.
My final objective is to predict the users that are not going to show up in week 2 according to their inapp experience during the 5 first days. 

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







