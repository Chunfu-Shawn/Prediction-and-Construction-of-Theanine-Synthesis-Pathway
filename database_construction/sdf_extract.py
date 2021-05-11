import re
import pandas as pd

with open('ChEBI_complete.sdf', 'r', encoding='UTF-8') as f:
    patstart = re.compile('  Marvin')
    patend = re.compile('M  END')
    pat2 = re.compile('> <ChEBI ID>')
    sdf = ''
    Flag = ''
    listSDF = []
    listID = []
    for line in f:
        if patstart.search(line):
            Flag = 'SDF'
        if patend.search(line):
            listSDF.append(sdf)
            Flag = 'SDFEND'
        if Flag == 'SDF':
            sdf = sdf + r'\n' + line
        if Flag == 'ID':
            listID.append(line)
            Flag = ''
        if pat2.search(line):
            Flag = 'ID'
    f.close()
    dp = pd.DataFrame({'ID': listID, 'SDF': listSDF})
    print(dp.values)
    dp.to_csv('compound_sdf.csv')
