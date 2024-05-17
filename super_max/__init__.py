"""
Code to run on Raspberry Pi for avionics applications 
"""

__author__ = "Benedict Rose; Zoe Cheah"
__version__ = "0.1.0"
__license__ = "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007"

import pandas as pd
import numpy as np 
import os
import itertools

def main():
    """
    Main script
    """
    # Constants
    # Number of races done so far
    RACES = 6
    # Number of drivers to select
    NUM_DRIVERS = 5
    # Number of constructors to select
    NUM_CONSTRUCTORS = 2
    # Cost cap
    COST_CAP = 100
    
    # Data url
    driver_data_url = "https://raw.githubusercontent.com/br3018/super-max/main/driver_info.csv"
    constructor_data_url = "https://raw.githubusercontent.com/br3018/super-max/main/constructor_info.csv"

    # Load data
    driver_df = pd.read_csv(driver_data_url)
    driver_df.info()
    print(driver_df.columns)
    constructor_df = pd.read_csv(constructor_data_url)
    constructor_df.info()
    print(constructor_df.columns)

    # Calculate expected points for each driver from historical data
    driver_df['expected_points'] = driver_df['points'].divide(RACES)
    # Calculate expected points for each constructor from historical data
    constructor_df['expected_points'] = constructor_df['points'].divide(RACES)

    # Generate combinations matrix for all drivers
    driver_combinations = list(itertools.combinations(driver_df['drivers'], 5))
    # Calculate expected score and cost for each team
    driver_combination_escore = np.zeros(len(driver_combinations))
    driver_combination_cost = np.zeros(len(driver_combinations))
    for i, driver_combination in enumerate(driver_combinations):
        driver_combination_escore[i] = driver_df[driver_df['drivers'].isin(driver_combination)]['expected_points'].sum()
        driver_combination_cost[i] = driver_df[driver_df['drivers'].isin(driver_combination)]['current_cost'].sum()
    
    # Generate combinations matrix for all constructors
    constructor_combinations = list(itertools.combinations(constructor_df['constructors'], 2))
    # Calculate expected score and cost for each team
    constructor_combination_escore = np.zeros(len(constructor_combinations))
    constructor_combination_cost = np.zeros(len(constructor_combinations))
    for i, constructor_combination in enumerate(constructor_combinations):
        constructor_combination_escore[i] = constructor_df[constructor_df['constructors'].isin(constructor_combination)]['expected_points'].sum()
        constructor_combination_cost[i] = constructor_df[constructor_df['constructors'].isin(constructor_combination)]['current_cost'].sum()

    # Combine driver and constructor combinations
    team_df = pd.DataFrame(columns=['driver_combination', 'constructor_combination', 'expected_score', 'cost'])
    for i, constructor_combination in enumerate(constructor_combinations):
        for j, driver_combination in enumerate(driver_combinations):
            team_df = team_df.append({'driver_combination': driver_combination, 'constructor_combination': constructor_combination, 'expected_score': driver_combination_escore[j] + constructor_combination_escore[i], 'cost': driver_combination_cost[j] + constructor_combination_cost[i]}, ignore_index=True)

    # Filter teams based on cost cap and sort by expected score
    team_df = team_df[team_df['cost'] <= COST_CAP].sort_values(by='expected_score', ascending=False)

    # Print top 20 teams 
    print(team_df.head(20))      
    

if __name__ == "__main__":
    main()