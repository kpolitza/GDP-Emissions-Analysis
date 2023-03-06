# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 14:46:11 2022

@author: polit
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import csv

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
    This function merges data into one frame and ensures that they have the same dimensions
    while dropping unneeded columns.
    """
    #drop unneeded columns
    gdp_raw = gdp.drop(columns=["Country Code", "Indicator Name", "Indicator Code", "Unnamed: 66"], axis=1)
    new_gdp = gdp_raw.melt(id_vars=["Country Name"])
    em_raw = em.drop(columns=["Country Code", "Indicator Name", "Indicator Code", "Unnamed: 66"], axis=1)
    new_em = em_raw.melt(id_vars=["Country Name"])
    
    #combine the frames
    combined = new_gdp
    combined["value 2"] = new_em["value"]
    
    combined = combined.rename(columns = {'value' : "GDP", 'value 2' : "Emissions"})
    
    return combined

def corr_testing(data):
    """
    This function performs both a Spearman and a Pearson correlation test on the dataframe.
    Each country over the range 1995-2017 has the test performed between GDP and Emissions.
    Returns two dictionaries.
    """
    test = data.dropna()
    
    col1 = "GDP"
    col2 = "Emissions"
    
    countries = test["Country Name"].tolist()
    last_country = countries[-1]
    last_country_index = countries.index(last_country)
    country_names = countries[0:last_country_index+1]
    
    p_correlation_dict = {}
    s_correlation_dict = {}
    
    for each in country_names:
        try:
            query = f"`Country Name` == '{each}'"
            country = test.query(query)
            year_range = country.query('variable >= "1995" and variable <= "2017"')
            #pearson correlation and spearman correlation
            p_corr = year_range[col1].corr(year_range[col2], method='pearson')
            s_corr = year_range[col1].corr(year_range[col2], method='spearman')
            p_correlation_dict[each] = round(p_corr, 3)
            s_correlation_dict[each] = round(s_corr, 3)
        except:
            pass
    
    #pearson test
    corr = test[col1].corr(test[col2], method='pearson')
    print("Pearson Correlation between ", col1, " and ", col2, "across all countries is: ", round(corr, 3))
    
    #spearman test
    corr = test[col1].corr(test[col2], method='spearman')
    print("Spearman Correlation between ", col1, " and ", col2, "across all countries is: ", round(corr, 3))
    
    return p_correlation_dict, s_correlation_dict
    
    
def no_nan_data_plotting(data):
    """
    This function plots the GDP v.s Emissions data in the form of a scatterplot for 
    all countries across all years. In essence, a distribution for the global GDP/Emissions data.

    """
    test = data.dropna()
    col1 = "GDP"
    col2 = "Emissions"
    
    X = test[col1]
    Y = test[col2]
    
    fig, ax = plt.subplots()
    ax.set_xlabel("GDP (USD)")
    ax.set_ylabel("Emissions (Metric Tons per Capita)")
    ax.set_title("GDP vs Emissions")
    
    ax.scatter(X,Y,color='b')
    
    fig.show()
    


if __name__ == "__main__":
    #load data and clean/tidy
    gdp, em = load_data()
    data = merge_data(gdp, em)
    pearson_corr_dict, spearman_corr_dict = corr_testing(data)
    
    #sort the dictionaries in descneding order
    sorted_pearson = {k: v for k, v in sorted(pearson_corr_dict.items(), reverse=True, key=lambda item: item[1])}
    sorted_spearman = {k: v for k, v in sorted(spearman_corr_dict.items(), reverse=True, key=lambda item: item[1])}
    no_nan_data_plotting(data)
    
    #generate text files to serve as a reference for analysis
    file = open("pearson_corr.txt", 'w')
    for each in sorted_pearson:
        s = str(each) + ": " + str(sorted_pearson[each]) + "\n"
        file.write(s)
        
    file.close()
    
    file = open("spearman_corr.txt", 'w')
    for each in sorted_spearman:
        s = str(each) + ": " + str(sorted_spearman[each]) + "\n"
        file.write(s)
        
    file.close()
    
    