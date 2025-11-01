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
    # Number of drivers to select
    NUM_DRIVERS = 5
    # Number of constructors to select
    NUM_CONSTRUCTORS = 2
    # Cost cap
    COST_CAP = 116.0

    # Get working directory
    cwd = os.getcwd()
    
    # Data url
    driver_data_url = "https://raw.githubusercontent.com/br3018/super-max/main/driver_info.csv"
    constructor_data_url = "https://raw.githubusercontent.com/br3018/super-max/main/constructor_info.csv"

    # Load data
    driver_df = pd.read_csv(driver_data_url)
    constructor_df = pd.read_csv(constructor_data_url)

    # Calculate expected points for each driver from historical data
    driver_df['expected_points'] = np.divide(driver_df['points'], driver_df['races'])
    # Calculate expected points for each constructor from historical data
    constructor_df['expected_points'] = np.divide(constructor_df['points'], constructor_df['races'])

    # Show dataframes
    print(driver_df.to_string())
    print()
    print(constructor_df.to_string())
    print()

    # Generate combinations matrix for all drivers
    print("Calculating driver combinations (1/3)")
    driver_combinations = list(itertools.combinations(driver_df['drivers'], 5))
    print("Found {} driver combinations".format(len(driver_combinations)))
    # Calculate expected score and cost for each team
    driver_combination_escore = np.zeros(len(driver_combinations))
    driver_combination_cost = np.zeros(len(driver_combinations))
    for i, driver_combination in enumerate(driver_combinations):
        # Find driver with highest expected points in combination (for applying DRS boost)
        driver_combination = list(driver_combination) # Convert driver combination to list to sort
        driver_combination.sort(key=lambda x: driver_df[driver_df['drivers'] == x]['expected_points'].values[0], reverse=True)
        # Calculate expected score and cost for each combination before DRS boost
        driver_combination_escore[i] = driver_df[driver_df['drivers'].isin(driver_combination)]['expected_points'].sum()
        driver_combination_cost[i] = driver_df[driver_df['drivers'].isin(driver_combination)]['current_cost'].sum()
        # Add double points for driver with highest expected points (DRS boost)
        driver_combination_escore[i] += driver_df[driver_df['drivers'] == driver_combination[0]]['expected_points'].values[0]
    print("Calculations complete")
    print()
    
    # Generate combinations matrix for all constructors
    print("Calculating constructor combinations (2/3)")
    constructor_combinations = list(itertools.combinations(constructor_df['constructors'], 2))
    print("Found {} constructor combinations".format(len(constructor_combinations)))
    # Calculate expected score and cost for each team
    constructor_combination_escore = np.zeros(len(constructor_combinations))
    constructor_combination_cost = np.zeros(len(constructor_combinations))
    for i, constructor_combination in enumerate(constructor_combinations):
        constructor_combination_escore[i] = constructor_df[constructor_df['constructors'].isin(constructor_combination)]['expected_points'].sum()
        constructor_combination_cost[i] = constructor_df[constructor_df['constructors'].isin(constructor_combination)]['current_cost'].sum()
    print("Calculations complete")
    print()


    # Combine driver and constructor combinations
    print("Calculating team combinations (3/3)")
    print("Found {} team combinations".format(len(driver_combinations) * len(constructor_combinations)))
    team_drivers = []
    team_constructors = []
    team_escore = []
    team_cost = []
    for i, constructor_combination in enumerate(constructor_combinations):
        print("{} Percent Complete".format(i/len(constructor_combinations) * 100))
        for j, driver_combination in enumerate(driver_combinations):
            team_drivers.append(driver_combination)
            team_constructors.append(constructor_combination)
            team_escore.append(driver_combination_escore[j] + constructor_combination_escore[i])
            team_cost.append(driver_combination_cost[j] + constructor_combination_cost[i])
    team_df = pd.DataFrame({'driver_combination': team_drivers, 'constructor_combination': team_constructors, 'expected_score': team_escore, 'cost': team_cost})
    print("Calculations complete")
    print()

    # Filter teams based on cost cap and sort by expected score
    team_df = team_df[team_df['cost'] <= COST_CAP].sort_values(by='expected_score', ascending=False)  

    # Save teams to csv
    path = os.path.join(cwd, "team_combinations.csv")
    print("Saving teams to {}".format(path))
    team_df.to_csv(path, index=False)

    print("Teams saved")
    print("Apply DRS boost to driver with highest expected points in combination")

if __name__ == "__main__":
    main()