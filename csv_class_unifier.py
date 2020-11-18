#imports
import pandas as pd
import numpy as np
import csv
import sys
import re

# args
args = {}
for arg in sys.argv[1:]:
  variable = re.search('\-(.*)\=',arg)
  variable = variable.group(1)
  value = re.search('\=(.*)',arg)
  value = value.group(1)
  args[variable] = value

# catch error
if ("i" not in args):
  print("Input --i is missing")

# read csv
cols = list(pd.read_csv(args['i'], nrows =1))
used_cols = ['id', 'location_x', 'location_y', 'operator', 'macro_classe_label','classe_label', 'micro_classe_label']

# clear dataframe
df = pd.read_csv(args['i'], usecols =[i for i in cols if i in used_cols])
df['class'] = ''

# for loop to unify classes
for index, row in df.iterrows():
  if(type(row['micro_classe_label']) != str):
    if(type(row['classe_label']) != str):
      df.loc[index, 'class'] = row['macro_classe_label']
    else:
      df.loc[index, 'class'] = row['classe_label']
  else:
    df.loc[index, 'class'] = row['micro_classe_label']

# drop old classes
df = df.drop(['macro_classe_label','classe_label', 'micro_classe_label'], axis=1)

# save
df.to_csv('new_'+args['i'], index = False)
