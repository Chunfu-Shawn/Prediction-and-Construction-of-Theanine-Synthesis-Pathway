import json
import pandas as pd

#打开json文件，并以表格形式打开为dfkegg
f = open('kegg_compounds.json')
info = json.load(f)
df_kegg = pd.DataFrame(info)
df_kegg = df_kegg.drop(columns=["num_electrons"])

df = pd.DataFrame(pd.read_csv('InChI_SDF.csv', sep=',', low_memory=False, index_col=0))
print(df_kegg.values)
df1 = pd.merge(df_kegg, df, how = "left", on ="InChI")

df1 = df1.dropna(subset=["InChI"])

df1 = df1.drop_duplicates(subset=['InChI'])
print(df1.values)
df1.to_csv("compound_InChI.csv", index=False)

f.close()