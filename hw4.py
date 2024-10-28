import pandas as pd
import seaborn.objects as sns
import numpy as np
import random
import matplotlib.pyplot as plt

"""
Dataset 1
Table 346 - Land and Water Area Of States and Other Entities: 2008

Q1: For each state, show the relationship between the state's land area and its total water area. 
Consider only the 50 US states (Alabama - Wyoming), ignore DC and the territories. 
Highlight any interesting outliers.

Q2: Pick 10 states and compare the proportion of their total area that is land and the proportion that is water.
You may pick the 10 states however you wish (e.g., 10 largest, 10 smallest, 10 largest based on land area, 10 largest based on water area, 10 favorite states),
but you must discuss how you chose the states.

Extra Credit [2 points]: Combine this table with Table 12 (Resident Population, from Section 1 - Population)
to show the relationship between land area and 2008 population for each state.
"""
INPUT_FILENAME_346="table_346_unrefined.csv"
INPUT_FILENAME_12="table_012_unrefined.csv"

OUTPUT_FILENAME_346="table_346.csv"
OUTPUT_FILENAME_12="table_012.csv"
OUTPUT_FILENAME_2008="table_012_and_346_2008.csv"
# Refine data method, cleans based on categories
# https://www.grepper.com/answers/824560/how+to+convert+a+pandas+string+column+to+numbers?ucard=1
# https://stackoverflow.com/questions/25698710/replace-all-occurrences-of-a-string-in-a-pandas-dataframe-python
# """
def refine_data(df, categories, misc=None):
    if misc:
        df.drop(misc, axis=1, inplace=True)
    df.replace('(X)', '0', inplace=True)
    for category in categories:
        df[category] = df[category].astype(str).replace(r'[\$\,]', '', regex=True).str.replace(r'\.\d*', '', regex=True).astype(int)
    return df
# https://www.grepper.com/answers/38631/apply+strip%28%29+a+column+in+pandas?ucard=1
def define_table_346(df):    
    # Define categories that need to be cast to ints
    str_to_int_categories = ['tot_square_mile','tot_square_kilom','land_square_mile','land_square_kilom',
                             'water_total_square_mile','water_total_square_kilom','inland_square_mile',
                             'coastal_square_mile','great_lakes_square_mile','territoraial_square_mile']
    df = refine_data(df, categories=str_to_int_categories, misc=['ehh?', 'Unnamed: 13', 'Unnamed: 11'])
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    return df

def sample_labels(labels, outliers, sample_rate=0.2):
    labels_1 = [""] * len(labels)
    for i in range(len(labels)):
        if not (labels[i] in outliers or random.random() <= sample_rate):
            labels_1[i] = ""
        else:
            labels_1[i] = labels[i]
    return labels_1

def define_table_12(df):
    # Define categories that need to be cast to ints
    str_to_int_categories = list(df.columns.values)[3:]
    
    # Remove whitespace and send to refined data method
    df.columns = [x.strip() for x in df.columns.values]
    df = refine_data(df, str_to_int_categories)
    
    # Remove month label from each year
    for column in str_to_int_categories:
        df.rename({column:column[:4]}, axis=1, inplace=True)
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    return df

"""
    Q1: For each state, show the relationship between the state's land area and its total water area. 
    Consider only the 50 US states (Alabama - Wyoming), ignore DC and the territories. 
    Highlight any interesting outliers.
"""
def question1(df):
    # Defining x and y values to plot
    x_vals = df['land_square_mile']
    y_vals = df['water_total_square_mile']
    # Defining and refining labels
    q1_outlier_states = ['Texas', 'California', 'Alaska', 'Michigan', 'New York', 'Florida', 'New Mexico', 'Montana']
    q1_labels = [x.strip() for x in list(df['State'])]
    q1_labels = sample_labels(labels=q1_labels, outliers=q1_outlier_states)
    colors = ['Red' if x in ['Alaska','Texas','Michigan'] else 'Blue' for x in q1_labels]
    
    # Scatter Plot
    plt.scatter(x=x_vals, y=y_vals, c=colors)
    plt.title("Relationship between land and water square miles by state")
    plt.xlabel("Total Area of Land (Square Miles)")
    plt.ylabel("Total Area of Water(Square Miles)")
    for i in range(len(q1_labels)):
        plt.text(x_vals[i], y_vals[i], q1_labels[i], fontdict={'family':'sans-serif', 'weight':'bold','size':7}, rotation=30, color='#ff7e30')
    #plt.savefig("Relationship_between_land_and_water_area.png")
    plt.show()
    plt.clf()

   

"""
    Q2: Pick 10 states and compare the proportion of their total area that is land and the proportion that is water.
    You may pick the 10 states however you wish (e.g., 10 largest, 10 smallest, 10 largest based on land area, 10 largest based on water area, 10 favorite states),
    but you must discuss how you chose the states.
"""
def question2(df):
    # Define category to sort by and filter the top 10 elements of
    category = 'tot_square_mile'
    
    # Finding elements in the top 10
    top_10 = df[df[category].isin(sorted(df[category], reverse=True)[:10])]
    
    # Defining data set to be plotted
    land_water_ratio = top_10['land_square_mile']/top_10['water_total_square_mile']
    
    # Sorting states by their land to water ratio
    sorted_vals = sorted(zip([x.strip() for x in list(top_10['State'])], land_water_ratio), key=lambda x: x[1], reverse=True)
    
    # Seperating the two lists to be plotted
    labels  = [x[0] for x in sorted_vals]
    heights = [x[1] for x in sorted_vals]

    # Bar Graph
    plt.title("Land to water ratio of top 10 states by total square mileage")
    plt.xlabel('States')
    plt.ylabel("Land/Water ratio")
    plt.bar(x=labels, height=heights)
    plt.xticks(rotation=45)
    #plt.savefig("Land_water_ratio_top_10_states.png")
    plt.show()
    plt.clf()

"""
    Extra Credit [2 points]: Combine this table with Table 12 (Resident Population, from Section 1 - Population)
    to show the relationship between land area and 2008 population for each state.
""" 
def bonus(df_346, df_12):
    # Defining fields and refining by fields for only information in table_12 2008
    new_df_fields = ['State', '2008']
    df_table_12_2008 = pd.DataFrame(df_12[new_df_fields])
    df_table_12_2008.rename(columns={'2008':'res_pop_2008'}, inplace=True)
    
    # Removing Non-states still in the data file
    remove_values = ['United States', 'Northeast','Midwest', 'South', 'West']
    df_table_12_2008 = df_table_12_2008[~df_table_12_2008['State'].isin(remove_values)]
    
    # Merging two datasets
    df_2008 = pd.merge(df_346, df_table_12_2008, on='State')
    
    # Defining data for presentation
    x_vals = df_2008['tot_square_mile']
    y_vals = df_2008['res_pop_2008']
    bonus_outlier_labels = ['Texas', 'California', 'Alaska', 'Michigan', 'New York', 'Florida', 'New Mexico', 'Montana']
    bonus_labels = df_2008['State']
    bonus_labels = sample_labels(labels=bonus_labels, outliers=bonus_outlier_labels, sample_rate=0.25)
    colors = ['Red' if x in ['Alaska','Texas', 'California', 'New York', 'Florida'] else 'Blue' for x in bonus_labels]

    # Scatter Plot
    plt.scatter(x=x_vals,y=y_vals, c=colors)
    plt.title("Residential Population vs Total Square miles by state (2008)")
    plt.xlabel("Total Square Miles")
    plt.ylabel("Residential Population in 2008")
    
    for i in range(len(bonus_labels)):
        plt.text(x_vals[i], y_vals[i], bonus_labels[i], fontdict={'family':'sans-serif', 'weight':'bold','size':7, 'color':'#ff7e30'}, rotation=30)
    
    #plt.savefig("Land_area_and_population_2008.png")
    plt.show()
    plt.clf()
    
    return df_2008
    
    

def main():
    plt.rcParams["figure.figsize"]=(10,9)
    df_table_346 = define_table_346(pd.read_csv(INPUT_FILENAME_346))
    df_table_346.to_csv(OUTPUT_FILENAME_346, index=False, encoding='utf-8')
    
    # question1(df_table_346)
    # question2(df_table_346)
    
    df_table_12 = define_table_12(pd.read_csv(INPUT_FILENAME_12))
    df_table_12.to_csv(OUTPUT_FILENAME_12, index=False, encoding='utf-8')
    
    df_table_12_346_2008 = bonus(df_table_346, df_table_12)
    df_table_12_346_2008.to_csv(OUTPUT_FILENAME_2008, index=False, encoding='utf-8')
if __name__ == "__main__":
    main()
