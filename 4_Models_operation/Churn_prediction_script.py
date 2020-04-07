# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 15:49:10 2020

"""

import pandas as pd
import glob
from functools import reduce
from sklearn.preprocessing import StandardScaler
from scipy.stats.mstats import winsorize
import pickle
import warnings; warnings.simplefilter('ignore')
import os

os.chdir(r'xxxx\Final models')
path = r'xxxx\Final models'
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)
    
df = reduce(lambda  left,right: pd.merge(left,right,on=['user_id'],how='outer'), [li[0], li[1], li[2], li[3], li[4]])
banned=li[5]

#CLEANING
### Dropping rows without user_id
df.drop(df[df.user_id.isna()].index,axis=0, inplace=True)
### user_gender : drop nan
df.drop(df[df.user_gender.isna()].index,axis=0, inplace=True)
### user_country : usually low level of missing value so we will fill it with FR (most represented country)
df.user_country.fillna('FR', inplace = True)
### max_connection_num: this col is nan when the user has not made anny connection during the 5 first days => fill with 0
df.max_connection_num.fillna(0, inplace = True)
### payments : the 4 payment columns are nan when the user has not made any purchase during the 5 first days => fill with 0
df.crowns_usd_5d.fillna(0, inplace = True)
df.sub_usd_5d.fillna(0, inplace = True)
df.sub_re_usd_5d.fillna(0, inplace = True)
df.discount_usd_5d.fillna(0, inplace = True)
### payments : replace subscription renewal by subscription 
df['sub_usd_5d'] = df.eval('sub_usd_5d + sub_re_usd_5d')
df.drop('sub_re_usd_5d', axis=1, inplace=True)
### crowns spent : same as previous
df.crowns_spent_pick_5d.fillna(0, inplace = True)
df.crowns_spent_more_pick_5d.fillna(0, inplace = True)
### ratings : same as previous
df.rating_given.fillna(0, inplace = True)
# Create a total login column
df['login_5d']= df.eval('1+d1+d2+d3+d4')
# Countries
def countries(x):
    top_lst = ['FR','IT', 'DE', 'BR', 'BE', 'CH', 'US', 'GB', 'AT', 'NL', 'CA']
    eur_lst = ['AL', 'AD', 'AM', 'BY', 'BA', 'BG', 'CY','CZ', 'DK', 'EE', 'ES', 'FO', 'FI',
               'GI','GR', 'HU', 'HR', 'IE', 'IS', 'LI', 'LT', 'LU', 'LV', 'MC', 'MK', 'MT', 'NO', 'PL', 'PT', 'RO', 'RU', 'SE', 'SI', 'SK', 'SM', 'TR', 'UA', 'VA']
    asia_lst = ['CN', 'YE', 'IN','AU','NZ', 'HK', 'JP', 'AF', 'AZ', 'BH', 'BD', 'BT', 'BN', 'KH', 'GE', 'ID', 'IR', 'IQ', 'IL', 'JO', 'KZ', 'KW', 'KG', 'LA', 'LB', 'MO', 'MY', 'MV', 'MN', 'MM', 'NP', 'KP', 'OM', 'PK', 'PH', 'QA', 'SA', 'SG', 'KR', 'LK', 'SY', 'TW', 'TJ', 'TH', 'TM', 'AE', 'UZ', 'VN']
    africa_lst = ['MA', 'CI','RE', 'DZ', 'NG', 'EG', 'TN','AE']
    southam_lst = ['MX','AR', 'CO','CL','PE', 'BO', 'BR', 'VG', 'CR', 'CU', 'CW', 'DM', 'DO', 'EC', 'SV', 'FK', 'GL', 'GP', 'GT', 'GY', 'HT', 'JM', 'NI', 'PA', 'PY', 'PR', 'BL', 'KN', 'LC', 'MF', 'PM', 'VC', 'SR', 'TT', 'UY', 'VE']
    if x in top_lst :
        return x
    elif x in eur_lst:
        return 'other EU'
    elif x in asia_lst:
        return 'other Asia'
    elif x in africa_lst:
        return 'other Africa'
    elif x in southam_lst:
        return 'other South America'
    else :
        return 'other'
df['country']= df.user_country.apply(lambda x: countries(x))
df.drop('user_country', axis=1, inplace=True)

# Acquisition
def paid(x):
    if x in ['Organic', 'Google Organic Search']:
        return 0
    else :
        return 1
df['paid_user'] = df.network.apply(lambda x: paid(x))
df.drop('network', axis=1, inplace=True)

# Drop banned accounts
banned['status']= 'banned'
banned.rename ( columns = {'Id' : 'user_id'}, inplace=True) 
df = df.merge(banned, on='user_id', how='left')
df.drop(df[df['status']=='banned'].index, inplace = True)
df.drop('status', axis=1, inplace= True)

# DATA PROCESSING
df1=df.copy()
# Drop install_date
df1.drop('install_date', axis=1, inplace=True)
# put user_id in index
df1.set_index('user_id', inplace = True)

# Age create bins
df1['age']= pd.cut(df1['user_age'], [18, 28, 38, 48,150], labels = [ '18_28','29-38', '38-48', 'more than 48'])
df1.drop('user_age', axis=1, inplace=True)
# Create dummies
col_dummies=['user_platform', 'country', 'age']
df1 = pd.get_dummies(data=df1, columns=col_dummies, drop_first=True)

# Transform crowns_usd_5d, sub_usd_5d, discount_usd_5d into dummies
df1['crowns_usd_5d']= df1.crowns_usd_5d.apply(lambda x: 1 if x>0 else 0)
df1['sub_usd_5d']= df1.sub_usd_5d.apply(lambda x: 1 if x>0 else 0)
df1['discount_usd_5d']= df1.discount_usd_5d.apply(lambda x: 1 if x>0 else 0)

# Transform connection into dummies
df1['connection']= df1.max_connection_num.apply(lambda x: 1 if x>0 else 0)
df1.drop('max_connection_num', axis=1, inplace=True)

# drop columns d1, d2, d3, d4
col_drop2 = ['d1', 'd2','d3', 'd4']
df1.drop(col_drop2, axis=1, inplace=True)

# Transform crowns usage columns into dummies
df1['crowns_spent_pick_5d']= df1.crowns_spent_pick_5d.apply(lambda x: 1 if x>0 else 0)
df1['crowns_spent_more_pick_5d']= df1.crowns_spent_more_pick_5d.apply(lambda x: 1 if x>0 else 0)

# split into 2 df : Men / Women
df1_m = df1[df1.user_gender=='m']
df1_w = df1[df1.user_gender=='w']

## MEN
# Keep colmns that have been kept after feature engineering
df1_m = df1_m[['crowns_usd_5d', 'sub_usd_5d', 'crowns_spent_pick_5d', 'rating_given',
       'login_5d', 'user_platform_web', 'country_BR', 'country_DE',
       'country_GB', 'country_NL', 'country_US', 'country_other Asia',
       'country_other South America', 'age_more than 48', 'connection']]
# Winsorize
winsorize(df1_m.rating_given,limits=[0,0.05],inplace=True)
# Scaling : creating of a df with scaled columns
scaler = StandardScaler()
df1_m[['login_5d','rating_given']] = scaler.fit_transform(df1_m[['login_5d','rating_given']])
# Import the men model
def unpickle_file(file_name):
    with open(file_name, 'rb') as in_file:
        return pickle.load(in_file)

model_m = unpickle_file('Men_churn_model_2')
# Make the prediction
y_pred_m = model_m.predict(df1_m)
# Add the prediction to the dataframe
df1_m['predicted_churn_w2'] = y_pred_m
df1_m['gender']= 'm'
# Get the final list
men_risk_churn=df1_m[['gender','predicted_churn_w2']][df1_m.predicted_churn_w2==1]

## WOMEN
# Keep colmns that have been kept after feature engineering
df1_w = df1_w[['sub_usd_5d', 'crowns_spent_more_pick_5d', 'login_5d', 'country_BE',
       'country_BR', 'country_CA', 'country_DE', 'country_FR', 'country_GB',
       'country_NL', 'country_US', 'country_other Africa', 'country_other EU',
       'country_other South America', 'age_more than 48']]
# Scaling : creating of a df with scaled columns
scaler = StandardScaler()
df1_w[['login_5d']] = scaler.fit_transform(df1_w[['login_5d']])

# Import the women model
model_w = unpickle_file('Women_churn_model_2')

# Make the prediction
y_pred_w = model_w.predict(df1_w)
# Add the prediction to the dataframe
df1_w['predicted_churn_w2'] = y_pred_w
df1_w['gender']= 'w'
# Get the final list
women_risk_churn=df1_w[['gender','predicted_churn_w2']][df1_w.predicted_churn_w2==1]

# Concatenate men and women in the same dataframe
result = pd.concat([men_risk_churn,women_risk_churn])

# Export final result
result.to_csv('churn_risk.txt', sep=' ', index = True)