import csv
import pandas as pd
import numpy as np
import kanonymize as ka
import cleandata as cd

df = pd.read_csv('HoustonCrimeData.csv', encoding='utf_8_sig', engine='python')
df = df.drop(['Occurrence Date', 'Occurrence Hour', 'NIBRS Class', 'Beat', 'Offense Count', 'Suffix'], axis=1)
df = cd.clean_data(df)
#print(df.head())
print(df.groupby('NIBRS Description').count().sort_values(['Incident']))
#IN algorithm, manually create address field yourself.
#print(df.groupby('Address').count())
print('df')
ka.k_anonymize(df, 5)
df.to_csv("anonymized_data.csv")
