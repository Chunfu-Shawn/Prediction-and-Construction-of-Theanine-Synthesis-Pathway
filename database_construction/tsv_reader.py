import numpy as np
import pandas as pd

# 打开compounds.tsv，调取ID和name，并按ID进行排序
df1 = pd.DataFrame(pd.read_csv('compounds.tsv', sep='\t',
                               usecols=[0, 5], low_memory=False))
df1.set_index('ID')
print(df1.info())
df1 = df1.sort_values(by=['ID'])
print(df1.values)

# 打开chemical_data.tsv，调取ID和formula，并按ID进行排序
df2 = pd.DataFrame(pd.read_csv('chemical_data.tsv', sep='\t',
                               usecols=[1, 3, 4], low_memory=False))
print(df2.info())

dfformula = df2.loc[df2['TYPE'].isin(['FORMULA'])]
dfmass = df2.loc[df2['TYPE'].isin(['MASS'])]
dfformula = dfformula.drop(columns=['TYPE'])
dfformula = dfformula.sort_values(by=['ID'])
print(dfformula.values)
print(df2.info())

# 将上面两个表取并集，以ID为common column
result1 = pd.merge(df1, dfformula, how='left', on='ID')

# 调取ID和mass，并按ID进行排序
dfmass = dfmass.drop(columns=['TYPE'])
dfmass = dfmass.sort_values(by=['ID'])
print(dfmass.values)

#将ID、name、formula和mass合并，以ID为common column
result2 = pd.merge(result1, dfmass, how='left', on='ID')
print(result2.values)
result2.to_csv('compound_1.csv')


df3 = pd.DataFrame(pd.read_csv('compound_1.csv', sep=',', low_memory=False))

df4 = pd.DataFrame(pd.read_csv('ChEBI_complete.csv', sep=',',
                               usecols=[5, 30], low_memory=False))

print(df3.dtypes)
#提取ChEBI：...后面其的数据，并将这一列变成int64型
df4['ID'] = df4['ID'].str[6:]
df4['ID'] = df4['ID'].astype(int)
print(df4.dtypes)
dfsmile = df4.sort_values(by=['ID'])
print(dfsmile.values)
#整合成一张表格
result3 = pd.merge(df3, dfsmile, how='left', on='ID')
print(result3.values)
result3.to_csv('compound_2.csv')