# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 12:13:00 2023

@author: User
"""

# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
#NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np

dataset_part_1 = 'file:///E:/IBM/Modul_10/dataset_part_1.csv'
df=pd.read_csv(dataset_part_1)
df.head(10)

df.isnull().sum()/df.shape[0]*100
df.dtypes

df.value_counts('LaunchSite')

df.value_counts('Orbit')


landing_outcomes = df.value_counts('Outcome')

for i,outcome in enumerate(landing_outcomes.keys()):
    print(i,outcome)
    
bad_outcomes=set(landing_outcomes.keys()[[1,3,5,6,7]])
bad_outcomes

landing_class = np.where(df['Outcome'].isin(set(bad_outcomes)), 0, 1)

df['Class']=landing_class
df[['Class']].head(8)

df.head(5)        

df["Class"].mean()

df.to_csv("dataset_part_2.csv", index=False)  
    
    