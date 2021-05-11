import json
import pandas as pd
import numpy as np

#打开json文件，并以表格形式打开为dfkegg
f = open('kegg_compounds.json')
info = json.load(f)
df_kegg = pd.DataFrame(info)
df_kegg = df_kegg.drop(columns=["num_electrons", "InChI"])
df_kegg = df_kegg.rename(columns={'KEGG_ID': 'CID'})

df = pd.DataFrame(pd.read_csv('compound_7.csv', sep=',', low_memory=False))
#给kegg所有compound加毒性
dftoxi = pd.DataFrame(pd.read_csv('search_data.csv', sep=',', usecols=[0, 1], low_memory=False, index_col=0))
df_kegg = pd.merge(df_kegg, dftoxi, how='left', on='CID')
#给kegg加上SMILE和SDF列，并将列排序
df_kegg['SMILES'] = np.nan
df_kegg['SDF'] = np.nan
order = ['CID','name','formula','mass','SMILES','toxicity','SDF']
df_kegg = df_kegg[order]
print(df_kegg.values)
df_kegg.to_csv("kegg_compound.csv")

#找compound_7里面有相同CID的kegg_compound的行
df_CID = df['CID'].values.tolist()
df2 = df_kegg.loc[df_kegg['CID'].isin(df_CID)]

#先将两个DataFrame融合为一个DataFrame；去掉当中公共的部分（使用drop_duplicates去重），则是不相交集合
df_rest = df_kegg.append(df2)
df_rest.drop_duplicates(keep=False, inplace=True)
print(df_rest.values)

#加到原表中
df.append(df_rest).to_csv("compound_end.csv", index=False)