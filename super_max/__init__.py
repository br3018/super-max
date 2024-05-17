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

    # Calcualate expected points for each driver from historical data
    driver_df['expected_points'] = driver_df['points'].divide(RACES)

    # Generate combinations matrix for all drivers
    driver_combinations = list(itertools.combinations(driver_df['drivers'], 5))
    # Calculate expected score for each team
    driver_combination_escore = np.zeros(len(driver_combinations))
    for i, driver_combination in enumerate(driver_combinations):
        driver_combination_escore[i] = driver_df[driver_df['drivers'].isin(driver_combination)]['expected_points'].sum()
    
    # Show driver combination and expected score
    print("Driver Combination and Expected Score")
    print("=====================================")
    for i in range(len(driver_combinations)):
        print(driver_combinations[i], driver_combination_escore[i])

if __name__ == "__main__":
    main()