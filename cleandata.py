import csv
import pandas as pd
import numpy as np
import kanonymize as ka
import cleandata as cd

# Standardizes data so it is more uniform and better for anonymizing.
def clean_data(df):
    #Counting uncommon ZIP codes
    uncommon_ZIP = []
    count_ZIP_df = df.groupby('ZIP Code').size().reset_index().rename(columns={0:'count'})
    #Gathering a list of all zip codes that are infrequent
    for index, row in count_ZIP_df.iterrows():
        if(row['count'] < 25):
            uncommon_ZIP.append(count_ZIP_df.at[index, 'ZIP Code'])
    for index, row in df.iterrows():
        #If any value is NULL (or nan), replace with "*" or "*****" if zip
        if(pd.isnull(row['ZIP Code'])):
            df.at[index, 'ZIP Code'] = "*****"
            row['ZIP Code'] = "*****"
            row['StreetName'] = "*"
            row['Block Range'] ="*"
            df.at[index, 'StreetName'] = "*"
            df.at[index, 'Block Range'] = "*"
        if(pd.isnull(row['Block Range'])):
            df.at[index, 'ZIP Code'] = "*****"
            row['ZIP Code'] = "*****"
            row['StreetName'] = "*"
            row['Block Range'] ="*"
            df.at[index, 'StreetName'] = "*"
            df.at[index, 'Block Range'] = "*"
        if(pd.isnull(row['StreetName'])):
            df.at[index, 'ZIP Code'] = "*****"
            row['ZIP Code'] = "*****"
            row['StreetName'] = "*"
            row['Block Range'] ="*"
            df.at[index, 'StreetName'] = "*"
            df.at[index, 'Block Range'] = "*"

           
        # If there's a - in Block Range, we will take the first number listed of the two
        if "-" in row['Block Range']:
            temp = row['Block Range'].split("-")[0]
            df.at[index,'Block Range'] = temp
        if row['ZIP Code'] in uncommon_ZIP:
            df = df.drop([index])
        elif len(row['ZIP Code']) > 5:
            # Any ZIPS that are larger than 5 are of size 10.  Removing 5 from their string.
            for i in range(5):
                df.at[index, 'ZIP Code'] = df.at[index, 'ZIP Code'][:-1]
        
    
    return df
                