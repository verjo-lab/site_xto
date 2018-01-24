# -*- coding: utf-8 -*-
import pandas as pd

df = pd.read_excel("s2_table_genomic_loc_of_lncrnas.xlsx")
df2 = pd.DataFrame()

f = open("smlincs_lista.txt")

df2["geneID"] = [x.strip() for x in f]


s1 = pd.merge(df, df2, how='inner', on=['geneID'])

s1.to_excel("smlincs_intersected.xlsx", index=None)

print(s1)