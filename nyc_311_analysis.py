# NYC 311 Complaint Anaylzer

# Fetches 311 complaint data from NYC’s Open Data API, categorizes complaint types, and outputs summary statistics

import requests # communication with web APIs
import pandas as pd  # library for data manipulation and analysis
import matplotlib.pyplot as plt  # creating graphs, charts, etc. for data visualization

def main():
    
    # Fetch data from NYC Open Data API
    url = "https://data.cityofnewyork.us/resource/erm2-nwe9.json?$limit=10000" # API endppoint of NYC 311 dataset, limited to 1000 records 
    data = requests.get(url).json() # fetch data from url and then convert into a Python list of dictionaries in JSON format
    df = pd.DataFrame(data) # convert list of dictionaries into a pandas DataFrame for easier data manipulation

    #print(df.columns) # test to see all columns in the dataset

    # User Input/Configuration
    startMsg = "NYC 311 Complaint Analyzer"
    print(startMsg)

    optionsMenu = "What data from 311 complaints would you like to analyze?\n" \
                "1. Top Complaint Types\n" \
                "2. Complaints by Borough\n" \
                "3. Complaints Over Time\n"
    print(optionsMenu)

    userChoice = input("Enter the number of your choice: ")
    if userChoice == '1':
        complaint_counts = top_complaint_types(df)
        display_and_export(complaint_counts, "Top Complaint Types", 'top_complaints.csv')
    elif userChoice == '2':
        borough_counts = complaints_by_borough(df)
        display_and_export(borough_counts, "Complaints by Borough", 'borough_distribution.csv')
    elif userChoice == '3':
        time_counts = complaints_over_time(df)
        display_and_export(time_counts, "Complaints Over Time", 'complaints_over_time.csv')
    else:
        print("Invalid choice. Please run again.")
        exit()
    
# Categorize and Analyze
def top_complaint_types(df):
    if 'complaint_type' not in df.columns:
        print("Error: 'complaint_type' column not found in dataset.")
        return pd.Series()
    df['complaint_type'] = df['complaint_type'].fillna('Unknown') # access "complaint_type" column in the DataFrame and handle any missing values by filling them with 'Unknown'
    complaint_counts = df['complaint_type'].value_counts().head(10) # count how many times each complaint type appears, limited to the top 10 complain types
    print(complaint_counts) # output the top 10 complaint types with their counts
    return complaint_counts

def complaints_by_borough(df):
    if 'borough' not in df.columns:
        print("Error: 'borough' column not found in dataset.")
        return pd.Series()
    borough_counts = df['borough'].value_counts()
    print(borough_counts)
    return borough_counts

def complaints_over_time(df):
    if 'created_date' not in df.columns:
        print("Error: 'created_date' column not found in dataset.")
        return pd.Series()
    df['created_date'] = pd.to_datetime(df['created_date'], errors='coerce') # convert the 'created_date' column to datetime format, handling errors by coercing invalid dates to NaT
    df = df.dropna(subset=['created_date']) # drop rows with NaT in 'created_date'
    df['date'] = df['created_date'].dt.date # extract date part only
    time_counts = df['date'].value_counts().sort_index() # count complaints per date and sort by date
    print(time_counts)
    return time_counts

# Visualization
def barChart(data, title):
    data.head(10).plot(kind='bar', title=title)
    plt.xlabel('Complaint Type')
    plt.ylabel('Number of Complaints')
    plt.tight_layout()
    plt.savefig(f"{title.replace(' ', '_').lower()}_bar_chart.png")
    plt.show()
        
def pieChart(data, title):
    data.plot(kind='pie', title=title, autopct='%1.1f%%')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig(f"{title.replace(' ', '_').lower()}_pie_chart.png")
    plt.show()
    
def lineChart(data, title):
    data.plot(kind='line', title=title)
    plt.xlabel('Date')
    plt.ylabel('Number of Complaints')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{title.replace(' ', '_').lower()}_line_chart.png")
    plt.show()

# Exporting Results
def export(data, filename):
    data.to_csv(filename)
    print(f"Data exported to {filename}")
    
def display_and_export(data, title, filename):
    
    print("\nSummary Data:")
    print(data)
    
    optionsMenu = "How would you like the data to be displayed?\n" \
                "1. Bar Chart\n" \
                "2. Pie Chart\n" \
                "3. Line Chart\n" 
    print(optionsMenu)
    
    userChoice = input("Enter the number of your choice: ")
    if userChoice == '1':
        barChart(data, title)
    elif userChoice == '2':
        pieChart(data, title)
    elif userChoice == '3':
        lineChart(data, title)
    else:
        print("Invalid choice. Please run the program again.")
        return
  
    #print(data)
    export(data, filename)
    
     
if __name__ == "__main__":
    main()


