import pandas as pd
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, parent_dir)
from Database.TypeFunctions import verifyCompositionID

def parse_helper(val):
    result = verifyCompositionID('', val)
    return pd.Series(result['Solvents']), pd.Series(result['Salts'])

print(os.path.join(current_dir, 'Inventory.csv'))
df = pd.read_csv(os.path.join(current_dir, 'Inventory.csv'))
df[['Solvents', 'Salts']] = df['CompositionID'].apply(parse_helper).apply(pd.Series)
print(df['CompositionID'])
print(df['Solvents'])