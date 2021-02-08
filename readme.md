# Data Security - K-Anonymity Project  
*This is for a school project and should only be used for education purposes*

For an University Project:
Chris Wszolek
Programmed and tested in Python 3.8.5

This application represents an effort to anonymize a dataset using privacy techniques taught in  
a college course on data privacy.  The main anonymization technique used was k-anonymity,
and several deployments of how to best apply this were looked into.  

The main question being saught was whether K-Anonymization was sufficient practice for
anonymizing data, or whether different techniques should be sought.  

The dataset used can be found in:
https://www.houstontx.gov/police/cs/Monthly_Crime_Data_by_Street_and_Police_Beat.htm
2019 data was the data used for this project.

The conclusion of this project was that k-anonymization offered a very expensive form of discovering  
the most least obscuring form of privatization, and even "common sense" solutions proved
difficult, thus a lot of useful information could be lost, making the dataset not useful.
The sensitive column is the "NIBRS Description" field.

First, the data is cleaned using algorithms in cleandata.py to make the forms more consistent.  
Some data is lost in the process of this.  Next, k-anonymization finding techniques are attempted,  
where a given k-value is used to determine how private the data should be.  The example used in
project.py uses k-value of 5.

- QI Values are [Block Range, StreetName, ZIP Code]
- Block Range Anonymization: Full - Remove first digit - Remove second digit - removed all digits
- StreetName Anonymization: Full - remove half of name - remove full name 
- ZIPCODE Anonymization: FULL - remove 1 digit at a time.