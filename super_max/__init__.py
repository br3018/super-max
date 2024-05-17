"""
Code to run on Raspberry Pi for avionics applications 
"""

__author__ = "Benedict Rose; Zoe Cheah"
__version__ = "0.1.0"
__license__ = "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007"

import pandas as pd
import numpy as np 
import os

def main():
    """
    Main script
    """
    # Constants
    RACES = 6
    
    # Data url
    data_url = "https://raw.githubusercontent.com/br3018/super-max/main/race_info.csv"

    # Load data
    df = pd.read_csv(data_url)
    df.info()

    # Calcualate expected points for each driver from historical data
    df["Expected Points"] = df["Points"]/RACES
    print(df.to_string())


if __name__ == "__main__":
    main()