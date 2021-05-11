import pandas as pd

df1 = pd.DataFrame(pd.read_csv("compound_InChI.csv", sep=',', low_memory=False,))
df2 = pd.DataFrame(pd.read_csv('sdf9.csv', sep=',', names=['InChI', 'SDF'], engine='python'))
print(df1.values)
print(df2.values)
df2 = df2.drop_duplicates(subset=['InChI'])

result = pd.merge(df1, df2, how='left', on='InChI')
print(result.values)
result.to_csv("compound_12.csv", index=False)
