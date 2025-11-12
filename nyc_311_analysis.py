# NYC 311 Complaint Anaylzer

# Fetches 311 complaint data from NYC’s Open Data API, categorizes complaint types, and outputs summary statistics

import requests # communication with web APIs
import pandas as pd  # library for data manipulation and analysis


# Fetch data from NYC Open Data API
url = "https://data.cityofnewyork.us/resource/erm2-nwe9.json?$limit=1000" # API endppoint of NYC 311 dataset, limited to 1000 records 
data = requests.get(url).json() # fetch data from url and then convert into a Python list of dictionaries in JSON format
df = pd.DataFrame(data) # convert list of dictionaries into a pandas DataFrame for easier data manipulation

#print(df.columns) # test to see all columns in the dataset

# Categorize and Analyze
df['complaint_type'] = df['complaint_type'].fillna('Unknown') # access "complaint_type" column in the DataFrame and handle any missing values by filling them with 'Unknown'
complaint_counts = df['complaint_type'].value_counts().head(10) # count how many times each complaint type appears, limited to the top 10 complain types
print(complaint_counts) # output the top 10 complaint types with their counts






