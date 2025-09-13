# super-max
Cheat code for finding optimal F1 fantasy teams

Method works based off extracting past performances for each F1 driver and calculating expected value of points scored per race. All combinations of F1 drivers and constructors are formulated and expected score for the selection is calculated. Option to then discard combinations which exceed the allowable budget. 

To run, enter most recent race data to constructor_info.csv and driver_info.csv from:
https://fantasy.formula1.com/en/statistics/details?tab=driver&filter=fPoints
Set COST_CAP according to your current cost cap and RACES according to how many races have happened so far. 

Improvements that could be made include incorporating the DRS feature and calculating expected points by number of races each driver has done rather than total. 