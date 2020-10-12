import numpy as np
import pandas as pd

import time
from tqdm import tqdm

import warnings
warnings.filterwarnings('ignore')


## cell towers
cell_towers = pd.read_csv('cell_tower_locations.csv')
print('-'*50 + '\n')
print(cell_towers.head())
print('\n',cell_towers.shape)
print('-'*50)


## data file
data_0 = pd.read_csv('1804010000.txt', sep='|', header=None)
data_0 = data_0.filter([0, 2, 9, 10, 11, 12, 13], axis=1)
print('\n'+'-'*50)
print(data_0.head())
print('\n',data_0.shape)
print('-'*50)


## define haversine distance
def haversine_dist(lat1, lon1, lat2, lon2):
    miles_constant = 3959
    lat1, lon1, lat2, lon2 = map(np.deg2rad, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1 
    dlon = lon2 - lon1 
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a)) 
    mi = miles_constant * c
    return mi



#### create clusters for cell towers, this will contain all the users present in the range of 2 mi from the cell tower

## this dict will contain all the clusters
clusters = {}

start = time.time()

for i, row in cell_towers.iterrows():
  ## calculate distance of all points in the data file from a cell tower
  data_0['distance'] = haversine_dist(row['latitude'], row['longitude'], data_0[11].values, data_0[10].values)
  ## create a dataFrame containing columns=[11, 10, 'distance'], this dataframe will only contain the vechicular locations which
  ## are at a distance<2 mi from the cell tower
  df = data_0[[11, 10, 'distance']][data_0['distance']<=2]

  ## create a dictionary from above dataframe
  tower_nbd = df.set_index([11, 10]).T.to_dict('list')

  ## append all into one big dictionary, append only if the dict tower_nbd is not empty
  if bool(tower_nbd)==True:
    clusters[(row['latitude'], row['longitude'])] = tower_nbd

finish = time.time()

print('\nTime taken to preprocess... ', finish-start)


## write results into a file
fout = 'CellTower_clusters.txt'

fo = open(fout, 'w')

for k, v in clusters.items():
    fo.write(str(k) + ': ' + str(v) + '\n\n')

fo.close()    



#### create clusters for users, this will contain all the cell towers present in the range of 2mi from the user

user_cluster = {}

start = time.time()


for i, row in data_0.iterrows():

    cell_towers['distance'] = haversine_dist(row[11], row[10], cell_towers['latitude'].values, cell_towers['longitude'].values)
    df = cell_towers[['latitude', 'longitude', 'distance']][cell_towers['distance']<=2]
    user_nbd = df.set_index(['latitude', 'longitude']).T.to_dict('list')

    if bool(user_nbd)==True:
      user_cluster[(row[11], row[10])] = user_nbd

finish = time.time()

print('\nTime needed to preprocess... ', finish-start)


## write the results into a file

f_out = 'User_clusters.txt'
fo = open(f_out, 'w')

for k, v in clusters.items():
  fo.write(str(k) + ': ' + str(v) + '\n\n')

fo.close()
