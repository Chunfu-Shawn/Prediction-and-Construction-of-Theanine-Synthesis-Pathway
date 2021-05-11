import pandas as pd
from rdkit import Chem
from rdkit.Chem import PandasTools

my_sdf_file = r'F:\python\ChEBI_complete.sdf'

frame = PandasTools.LoadSDF(my_sdf_file,
                            smilesName='SMILES',
                            molColName='Molecule',
                            includeFingerprints=False)

frame.to_csv(r'F:\python\ChEBI_complete.csv')
