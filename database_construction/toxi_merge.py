import pandas as pd
df1 = pd.DataFrame(pd.read_csv("compound_InChI.csv", sep=',', low_memory=False, index_col=0))
dftoxi = pd.DataFrame(pd.read_csv('search_data.csv', sep=',', usecols=[0, 1], low_memory=False, index_col=0))

print(df1.dtypes)
print(dftoxi.dtypes)
df2 = pd.merge(df1, dftoxi, how='left', on='CID')
df2.to_csv("compound_InChI2.csv")