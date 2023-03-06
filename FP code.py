# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 14:46:11 2022

@author: liamorcutt
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

def load_data():
    """
    This function loads the data from csv files into dataframes
    """
    path = os.getcwd() + "\\data\\"
    gdp_file = "gdp_by_country.csv"
    em_file = "emissions_by_country.csv"
    
    gdp = pd.read_csv((path + gdp_file))
    em = pd.read_csv((path + em_file))
    
    return gdp, em

def merge_data(gdp, em):
    """
    This function merges data into one frame and ensures that they have the same dimensions.
    """
    #drop unneeded columns
    gdp_raw = gdp.drop(columns=["Country Code", "Indicator Name", "Indicator Code"], axis=1)
    new_gdp = gdp_raw.melt(id_vars=["Country Name"])
    em_raw = em.drop(columns=["Country Code", "Indicator Name", "Indicator Code"], axis=1)
    new_em = em_raw.melt(id_vars=["Country Name"])
    
    #combine the frames
    combined = new_gdp
    combined["value 2"] = new_em["value"]
    
    combined = combined.rename(columns = {'value' : "GDP", 'value 2' : "Emissions"})
    
    return combined

def corr_testing(data):
    """
    This function performs a Pearson correlation test on the dataframe.
    """
    test = data.dropna()
    col1 = "GDP"
    col2 = "Emissions"
    
    #pearson test
    corr = test[col1].corr(test[col2], method='pearson')
    print("Pearson Correlation between ", col1, " and ", col2, "is: ", round(corr, 3))
    
    #spearman test
    corr = test[col1].corr(test[col2], method='spearman')
    print("Spearman Correlation between ", col1, " and ", col2, "is: ", round(corr, 3))
    
    
def no_nan_data_plotting(data):
    test = data.dropna()
    col1 = "GDP"
    col2 = "Emissions"
    
    X = test[col1]
    Y = test[col2]
    
    fig, ax = plt.subplots()
    ax.set_xlabel("GDP")
    ax.set_ylabel("Emissions")
    ax.set_title("GDP vs Emissions")
    
    ax.scatter(X,Y,color='b')
    
    fig.show()
    
def count_na(data):
    '''
    This function counts the total NAs of GDP and Emissions.
    It also creates a dictionary for both GDP and Emissions that counts
    the number of NAs each year.
    '''
    #Create variables
    total_GDP_na = 0
    total_em_na = 0
    GDP_dict = {}
    em_dict = {}
    
    #For loop to loop through each line of data
    for i in range(0,len(data)):
        
        #Get variables from line
        GDP = data.iloc[i][2]
        emissions = data.iloc[i][3]
        year = data.iloc[i][1]
        
        #Count NA for GDP
        if np.isnan(GDP):
            total_GDP_na += 1
            if year in GDP_dict:
                GDP_dict[year] += 1
            else:
                GDP_dict[year] = 1
                
        #Count NA for emissions
        if np.isnan(emissions):
            total_em_na += 1
            if year in em_dict:
                em_dict[year] += 1
            else:
                em_dict[year] = 1
    
    #Print data
    print(total_GDP_na, total_em_na)
    print("GDP Dictionary", GDP_dict)
    print('\n')
    print("Emissions Dictionary", em_dict)
    #Appears years 1995 - 2017 would be best
    
    #Print scatterplot
    x = GDP_dict.keys()
    y = GDP_dict.values()
    plt.scatter(x,y)
    plt.show()

if __name__ == "__main__":
    gdp, em = load_data()
    data = merge_data(gdp, em)
    corr_testing(data)
    no_nan_data_plotting(data)