import requests
import numpy as np
from collections import defaultdict

# Your data
Missions=defaultdict(dict)  #  Missions: period, priority, 
Missions['BM']=[ 1, 1]  #Burn Site Resource Monitoring (human and equipment)
Missions['FI']=[ 0.25, 1]  #Fire Intensity Inspection 
Missions['FT']=[ 0.5, 1]  # track the fire perimeter and the risky area (arrival within 10 min)
Missions['FD']=[ 0.5, 1] # Fire detection

my_array = np.zeros((3, 4))
Size=(3,4)### Fire Setting Grid Size
Grid_map=np.full((Size[0],Size[1]),0)
Grid_map[0,0]=0
Grid_map[0,3]=1
Grid_map[1,3]=1
Res=0.5 # Grid size
Plan=1
Wind=10
Direction=271
# Convert data to JSON
data = {
    'Missions': Missions,
    'Grid_map': Grid_map.tolist(), 'Plan': Plan, 'Wind':Wind,'Direction': Direction}# Convert NumPy array to list for JSON serialization

# Send POST request
url = 'https://http://192.168.82.130:5000/'
response = requests.post(url, json=data)

# Check response status code
if response.status_code == 200:
    print('POST request successful!')
else:
    print('POST request failed with status code', response.status_code)