import pandas as pd

df1 = pd.DataFrame(pd.read_csv("compound_rest.csv", sep=',', low_memory=False))
df2 = pd.DataFrame(pd.read_csv('compound_6.csv', sep=',', low_memory=False))
df1 = df1.drop(columns=['InChI'])
df2 = df2.drop(columns=['ID'])

#找到在compound_6.csv中存在的compound_rest.csv行
df2_CID = df2['CID'].values.tolist()
df = df1.loc[df1['CID'].isin(df2_CID)]
#先将两个DataFrame融合为一个DataFrame；去掉当中公共的部分（使用drop_duplicates去重），则是不相交集合
df_rest = df1.append(df)
df_rest.drop_duplicates(keep=False, inplace=True)
print(df_rest.values)
print(df2.dtypes)

#改变列顺序并加到原表中
order = ['CID','Name','formula','MASS','SMILES','toxicity','SDF']
df_rest = df_rest[order]
df2.append(df_rest).to_csv("compound_7.csv", index=False)
