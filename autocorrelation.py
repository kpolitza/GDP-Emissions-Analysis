# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 14:46:11 2022

@author: polit
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
from statsmodels.graphics.tsaplots import plot_acf


def load_data():
    """
    This function loads the data from csv files into dataframes
    """
    path = os.getcwd() + "/data/"
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
    gdp_raw = gdp.drop(columns=["Country Code", "Indicator Name", "Indicator Code", "Unnamed: 66"], axis=1)
    new_gdp = gdp_raw.melt(id_vars=["Country Name"])
    em_raw = em.drop(columns=["Country Code", "Indicator Name", "Indicator Code", "Unnamed: 66"], axis=1)
    new_em = em_raw.melt(id_vars=["Country Name"])
    print(new_em)
    print(new_gdp)
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
            #print("Pearson Correlation between ", col1, " and ", col2, " for ", each, " is: ", round(corr, 3))
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
    


if __name__ == "__main__":
    gdp, em = load_data()
    data = merge_data(gdp, em)
    pearson_corr_dict, spearman_corr_dict = corr_testing(data)
    print(pearson_corr_dict)
    print(spearman_corr_dict)
    no_nan_data_plotting(data)
    
    
def autocorrelation(data):
    
    test = data.dropna()
    
    test = test[(test['Country Name'] != 'Somalia')]
    test = test[(test['Country Name'] != 'Venezuela, RB')]
    test = test[(test['Country Name'] != 'Mali')]
    #really ugly code i used to take out the variables that dont include all data points

    
    
    countries = test["Country Name"].tolist()
    last_country = countries[-1]
    last_country_index = countries.index(last_country)
    country_names = countries[0:last_country_index+1]

    
    for each in country_names:
        try:
            cName = test[(test['Country Name'] == each)]
            #print(cName)
            cName = cName[(cName['variable'] >= "1995")]
            #print(cName)
            cName = cName[(cName['variable'] <= "2017")]
            #print(cName)

            #pearson correlation and spearman correlation
            cName = cName[['variable','GDP']].set_index(['variable'])
            #print(cName)

            #print(each)
            #print(cName)
            #venezuela, RB is missing data from 2015-2017, so it cannot be ran in the loop
            #somalia is also missing data, from 1995-2012
            
           
            plot_acf(cName,lags=22, title = each)
            
            

        except:
            pass
        
        #the graph shows the autocorrelation coefficient for each country from 1995-2017
        #We can see that on most graphs, it approaches 0 at around 7/8 years lag, and that it 
        #peaks at minimum correlation at around 15 years of lag and then approaches 0
        
        
        