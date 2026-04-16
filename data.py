import pandas as pd

dff=pd.read_csv('patients.csv')
print(dff.head())
pd.set_option('display.max_columns', None)
print(dff.head(56))
