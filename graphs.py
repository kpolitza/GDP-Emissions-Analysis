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

    Parameters
    ----------
    data : pandas dataframe
        The dataframe containing the country with corresponding GDP and emissions values for each year

    Returns
    -------
    GDP_dict : python dictionary
        The dictionary containing the # of missing GDP data for every year for every country
    em_dict : python dictionary
        The dictionary containing the # of missing emissions data for every year for every country

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
        year = int(data.iloc[i][1])
        
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
    
    #Return dictionaries of GDP and Emissions values
    return GDP_dict, em_dict

def graph_na(GDP_dict, em_dict):
    
    #Create and print scatterplot of % of Countries Missing Data by Year
    TOTAL_COUNTRIES = 266 #Declare constant for total # of countries
    
    #GDP scatterplot data
    x = GDP_dict.keys() # Get years for x axis
    y = []
    for val in GDP_dict.values(): # Get y axis values
        y.append(val/TOTAL_COUNTRIES) # Convert to %
    plt.scatter(x,y, s = 3, alpha = .5, label = 'GDP')
    
    #Emissions scatterplot data
    y = []
    for val in em_dict.values(): # Get y axis values
        y.append(val/TOTAL_COUNTRIES) 
    plt.scatter(x,y, s = 3, alpha = .5, label = 'Emissions')
    
    #Format scatterplot
    plt.title('% of Countries Missing Data by Year')
    plt.xlabel('Year')
    plt.ylabel('% of Countries Missing Data')
    plt.legend()
    plt.show()

def graph_GDP_em(data, country_list):
    '''
    This function creates a scatterplot of both GDP and emissions by year for each country 
    listed in the country_list parameter.
    
    Parameters
    ----------
    data : pandas dataframe
        The dataframe containing the country with corresponding GDP and emissions values for each year
    country_list : list
        A list of strings containing country names to be graphed

    Returns
    -------
    None.

    '''
    #Create dictionaries for GDP and Emissions with a key for every country in country_list
    top_GDP_dict = {}
    top_em_dict = {}
    for country in country_list:
        top_GDP_dict[country] = []
        top_em_dict[country] = []
    
    #Add data values to the corresponding list in the dictionaries
    for i in range(0,len(data)):
        if data.iloc[i][0] in country_list:
            for country in country_list:
                if data.iloc[i][0] == country:
                    top_GDP_dict[country].append(data.iloc[i][2])
                    top_em_dict[country].append(data.iloc[i][3])
    
    #Create a list of the years we are studying
    year_list = []
    for i in range(1960,2022):
        year_list.append(i)
    
    #Create a scatterplot for each country in country_list
    for country in top_GDP_dict:
        fig, ax = plt.subplots(figsize = (10, 5))
        ax2 = ax.twinx() # For getting a second y axis
        
        x = year_list
        y = top_GDP_dict[country] # GDP
        ax.scatter(x,y, color = 'g', alpha = .5)
        
        y2 = top_em_dict[country] # Emissions
        ax2.scatter(x,y2, color = 'b', alpha = .5)
        
        #labels and formatting
        ax.set_xlabel('Year')
        ax.set_ylabel('GDP per capita (current USD)', color = 'g')
        ax2.set_ylabel('CO2 Emissions (metric tons per capita)', color = 'b')
        plt.title(country)
        
        plt.show()
    
        

def main():
    gdp, em = load_data()
    data = merge_data(gdp, em)
    corr_testing(data)
    GDP_dict, em_dict = count_na(data)
    graph_na(GDP_dict, em_dict)
    
    #specify which country to plot here
    country_list = ['India', 'China', 'United States', 'Qatar', 'Japan', 'East Asia & Pacific', 'North America']
    graph_GDP_em(data, country_list)
