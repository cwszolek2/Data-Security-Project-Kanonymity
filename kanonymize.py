import csv
import pandas as pd
import numpy as np
import copy

# QI Values are [Block Range, StreetName, ZIP Code]
# Block Range Anonymization: Full - Remove first digit - Remove second digit - removed all digits
# StreetName anonymization: Full - remove half of name - remove full name
# ZIPCODE Anonymization: FULL - remove 1 digit at a time.
QI_ARRAY = [4, 2, 5]
CURRENT_ARRAY = [0, 0, 0]

class QI_Count:
    def __init__(self, value, num):
        self.value = value
        self.num = num

#QI_ARRAY will be used as a global variable for this specific dataset
def k_anonymize(df, k_value):
    qi_list = []
    print("1")
    freq_list = make_freq_list(df)

    print("2")
    print(freq_list)
    count = 1
    #Not sure what the second part of the while loop is about or how to incorporate it.
    # Every third time around, will remove one digit from ZIP Code
    # TODO - consider how empty zip codes mess up this algorithm
    while(freq_list['count'] < k_value).any():
        #Third time, just doing ZIP code anon, skipping rest of loop
        if count % 3 == 0 and count != 0:
            df = anonymize_attribute(df, "ZIP Code")
            freq_list = make_freq_list(df)
            # freq_check_duplicates is O(n^2), so we limit it to smaller freq_lists
            #if count > 3:
            #    freq_check_duplicates(freq_list, k_value)
       
            count = count + 1
            continue
        most_uniq = find_uniq_values(df)
        df = anonymize_attribute(df, most_uniq)
        print(df.head())
        if isinstance(df, bool):
            print("uh oh")
            exit(1)
        freq_list = make_freq_list(df)
        print(freq_list)
        count = count + 1
    print(df.head())
        
# Requires dataframe
# Makes a list of the frequency of a specific set of tuples.  
def make_freq_list(df):
    freq_list = df.groupby(['ZIP Code', 'StreetName', 'Block Range']).size().reset_index().rename(columns={0:'count'}).sort_values(['count']).reset_index(drop=True)
    #Dropping any value where item is already anonymized from frequency list, as it shouldn't be counted.
    for index, row in freq_list.iterrows():
        if(row['ZIP Code'] == "*****" and row['StreetName'] == "*" and row['Block Range'] == "*"):
            freq_list.drop([index])

    return freq_list

#This method looks to see if the ZIP code = "*****" and NIBRS, Block Range, and StreetName = another value.  If so, it will delete the 
#row and add one to the count of the other value.
def freq_check_duplicates(freq_list, k_value):
    for index, row in freq_list.iterrows():
        print("index" + str(index))
        if row['ZIP Code'] == "*****" and row['count'] < k_value:
            print('True')
            temp_s = row['StreetName']
            temp_b = row['Block Range']
            temp_count = row['count']
            for index_2, row_2 in freq_list.iterrows():
                if row['ZIP Code'] != "*****" and temp_s == row_2['StreetName'] and temp_b == row_2['Block Range']:
                    freq_list.at[index_2, 'count'] = freq_list.at[index_2, 'count'] + temp_count
                    freq_list.drop([index])
                    break
    return freq_list

#Finds the column with the most unique values
def find_uniq_values(df):
    zipc = len(pd.unique(df['ZIP Code']))
    street = len(pd.unique(df['StreetName']))
    block = len(pd.unique(df['Block Range']))
    vmax = max(zipc, street, block)
    if vmax == zipc:
        return "ZIP Code"
    if vmax == street:
        return "StreetName"
    if vmax == block:
        return "Block Range" 

def anonymize_attribute(df, attribute_string):
    if attribute_string == "ZIP Code":
        if CURRENT_ARRAY[2] == 0:
            for index, row in df.iterrows():
                if pd.isnull(row['ZIP Code']):
                    continue
                temp = row['ZIP Code']
                temp = list(temp)
                temp[4] = "*"
                temp = ''.join(map(str, temp))
                df.at[index, 'ZIP Code'] = temp
            CURRENT_ARRAY[2] = 1
            return df
        elif CURRENT_ARRAY[2] == 1:
            for index, row in df.iterrows():
                if pd.isnull(row['ZIP Code']):
                    continue
                temp = row['ZIP Code']
                temp = list(temp)
                temp[3] = "*"
                temp = ''.join(map(str, temp))
                df.at[index, 'ZIP Code'] = temp
            CURRENT_ARRAY[2] = 2
            return df
        elif CURRENT_ARRAY[2] == 2:
            for index, row in df.iterrows():
                if pd.isnull(row['ZIP Code']):
                    continue
                temp = row['ZIP Code']
                temp = list(temp)
                temp[2] = "*"
                temp = ''.join(map(str, temp))
                df.at[index, 'ZIP Code'] = temp
            CURRENT_ARRAY[2] = 3
            return df
        elif CURRENT_ARRAY[2] == 3:
            for index, row in df.iterrows():
                if pd.isnull(row['ZIP Code']):
                    continue
                temp = row['ZIP Code']
                temp = list(temp)
                temp[1] = "*"
                temp = ''.join(map(str, temp))
                df.at[index, 'ZIP Code'] = temp
            CURRENT_ARRAY[2] = 4
            return df
        elif CURRENT_ARRAY[2] == 4:
            for index, row in df.iterrows():
                if pd.isnull(row['ZIP Code']):
                    continue
                temp = row['ZIP Code']
                temp = list(temp)
                temp[0] = "*"
                temp = ''.join(map(str, temp))
                df.at[index, 'ZIP Code'] = temp
            CURRENT_ARRAY[2] = 5
            return df
        elif CURRENT_ARRAY[2] == 5:
            print(df.head())
            print("Shouldn't be here1")
            return False
        #anything higher than this shouldn't be possible
    elif attribute_string == "StreetName":
        if CURRENT_ARRAY[1] == 0:
            for index, row in df.iterrows():
                if pd.isnull(row['StreetName']):
                    continue
                temp = row['StreetName']
                length = len(row['StreetName'])
                temp = list(temp)
                #Cutting the string in half
                for i in range(int(length/2)):
                    temp = temp[:-1]
                #Adding a * to the end of the half
                temp = ''.join(map(str, temp))
                temp = temp + "*"
                df.at[index, 'StreetName'] = temp
            CURRENT_ARRAY[1] = 1
            return df
        elif CURRENT_ARRAY[1] == 1:
            for index, row in df.iterrows():
                if pd.isnull(row['StreetName']):
                    continue
                df.at[index, 'StreetName'] = "*"
            CURRENT_ARRAY[1] = 2
            return df
        elif CURRENT_ARRAY[1] == 2:
            print(df.head())
            print("Shouldn't be here.2")
            return False
    elif attribute_string == "Block Range":
        if CURRENT_ARRAY[0] == 0:
            for index, row in df.iterrows():
                if pd.isnull(row['Block Range']):
                    continue
                if row['Block Range'] == "*":
                    continue
                temp = row['Block Range']         
                if int(temp) < 1000:
                    df.at[index, 'Block Range'] = "< 1000"
                elif int(temp) >= 1000 and int(temp) < 2000:
                    df.at[index, 'Block Range'] = ">= 1000 < 2000"
                elif int(temp) >= 2000 and int(temp) < 3000:
                    df.at[index, 'Block Range'] = ">= 2000 < 3000"
                elif int(temp) >= 3000 and int(temp) < 4000:
                    df.at[index, 'Block Range'] = ">= 3000 < 4000"
                elif int(temp) >= 4000 and int(temp) < 5000:
                    df.at[index, 'Block Range'] = ">= 4000 < 5000"
                elif int(temp) >= 5000 and int(temp) < 6000:
                    df.at[index, 'Block Range'] = ">= 500 < 600"
                elif int(temp) >= 6000 and int(temp) < 7000:
                    df.at[index, 'Block Range'] = ">= 6000 < 7000"
                elif int(temp) >= 7000 and int(temp) < 8000:
                    df.at[index, 'Block Range'] = ">= 7000 < 8000"
                elif int(temp) >= 8000 and int(temp) < 9000:
                    df.at[index, 'Block Range'] = ">= 8000 < 9000"
                elif int(temp) >= 9000 and int(temp) < 10000:
                    df.at[index, 'Block Range'] = ">= 9000 < 10000"
                elif int(temp) >= 10000:
                    df.at[index, 'Block Range'] = ">= 10000"
            CURRENT_ARRAY[0] = 1
            return df
        elif CURRENT_ARRAY[0] == 1:
            for index, row in df.iterrows():
                if pd.isnull(row['Block Range']):
                    continue
                temp = row['Block Range']
                if temp == "< 1000":
                    df.at[index, 'Block Range'] = "< 2000"
                elif temp == ">= 1000 < 2000":
                    df.at[index, 'Block Range'] = "< 2000"
                elif temp == ">= 2000 < 3000":
                    df.at[index, 'Block Range'] = ">= 2000 < 4000"
                elif temp == ">= 3000 < 4000":
                    df.at[index, 'Block Range'] = ">= 2000 < 4000"
                elif temp == ">= 4000 < 5000":
                    df.at[index, 'Block Range'] = ">= 4000 < 6000"
                elif temp == ">= 5000 < 6000":
                    df.at[index, 'Block Range'] = ">= 4000 < 6000"
                elif temp == ">= 6000 < 7000":
                    df.at[index, 'Block Range'] = ">= 6000 < 8000"
                elif temp == ">= 7000 < 8000":
                    df.at[index, 'Block Range'] = ">= 6000 < 8000"
                elif temp == ">= 8000 < 9000":
                    df.at[index, 'Block Range'] = ">= 8000 < 10000"
                elif temp == ">= 9000 < 10000":
                    df.at[index, 'Block Range'] = ">= 8000 < 10000"
                else:
                    df.at[index, 'Block Range'] = ">= 10000"
            CURRENT_ARRAY[0] = 2
            return df
        elif CURRENT_ARRAY[0] == 2:
            for index, row in df.iterrows():
                if pd.isnull(row['Block Range']):
                    continue
                temp = row['Block Range']
                if temp == "< 2000" or temp == ">= 2000 < 4000":
                    df.at[index, 'Block Range'] = "< 4000"
                elif temp == ">= 4000 < 6000" or temp == ">= 6000 < 8000":
                    df.at[index, 'Block Range'] = ">= 4000 < 8000 "
                elif temp == ">= 8000 < 10000" or temp == ">= 10000":
                    df.at[index, 'Block Range'] = ">= 8000"
            CURRENT_ARRAY[0] = 3
            return df

