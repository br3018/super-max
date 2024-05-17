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
    # Get current working directory
    cwd = os.getcwd()

    # Load data
    data_path = os.path.join(cwd, "race_info.csv")
    print(data_path)
    df = pd.read_csv(data_path)
    df.info()


if __name__ == "__main__":
    main()