#%% 
## Project Name: mia1
### Program Name: mia1_audiofiles.py
### Purpose: To download audio data of MIA Collections. 
##### Date Created: Mar 2nd 2021
import os 
import pathlib
import requests
import json
import pandas as pd
import numpy as np
import re
APP_PATH = str(pathlib.Path(__file__).parent.resolve())
#%% 
# Read in objects from the csv file 
# (objects csv file created in mia1_data.py)
obj=pd.read_csv(os.path.join(APP_PATH, 'data/objects.csv'))
objid=list(obj['obj_id'])
apiurl='https://search.artsmia.org/id/'

# %% 
# Identify objects with audio files
audiolinks=dict()
count=0
for i in objid:
    metajurl=apiurl+str(i)
    metaj=requests.get(metajurl).json()
    if 'related:audio-stops' in metaj.keys():
        print('id:',str(i), 'index:',str(count))
        audiolinks[str(i)]=metaj['related:audio-stops'][0]['link']
    count+=1
# %%
# Save audiolinks dictionary to cvs
audio_pd=pd.DataFrame.from_dict(audiolinks, orient='index')
audio_pd.columns=['audiolink']
audio_pd.to_csv(os.path.join(APP_PATH, 'data/audiolinks.csv'),
        index=True, header=True)
# %%
# Cleanup
del apiurl, audiolinks, count, i, metaj, metajurl, objid
#%%
# Find image urls for the audio stops
objid=list(audio_pd['id'].values)
#%%
imglinks=dict()
count=0
for id in objid:
    url='https://collections.artsmia.org/art/'+str(id)
    url_r = requests.get(url)
    x=url_r.text
    pattern="https://[0-9].api.artsmia.org/"+str(id)+".jpg"
    imgurls=list(set(re.findall(pattern, x)))
    imglinks[id]=imgurls
    count+=1
# %%
# Save imglinks dictionary to cvs
img_pd=pd.DataFrame.from_dict(imglinks, orient='index')
img_pd.columns=['imglink']
img_pd.to_csv(os.path.join(APP_PATH, 'data/imglinks.csv'),
        index=True, header=True)
#%%
# Load audio and image links data from csv 
# (data saved externally so that the script can be 
# run across different sessions)
audio_pd=pd.read_csv(os.path.join(APP_PATH, 'data/audiolinks.csv'),index_col=False)
img_pd=pd.read_csv(os.path.join(APP_PATH, 'data/imglinks.csv'),index_col=False)
img_pd.columns=['id','imglink']
#%%
#% Download audio files
for index,row in audio_pd.iterrows():
    filename=os.path.join(APP_PATH,'data/audio',str(row['id'])+'.mp3')
    r = requests.get(row['audiolink'])
    with open(filename, 'wb') as f:
        f.write(r.content)
f.close()
del f, r, filename, index, row
#%%
#% Download image files
for index,row in img_pd.iterrows():
    filename=os.path.join(APP_PATH,'data/img',str(row['id'])+'.jpg')
    r = requests.get(row['imglink'])
    with open(filename, 'wb') as f:
        f.write(r.content)
f.close()
del f, r, filename, index, row
# %%
#Cleanup
del objid, id, url, url_r, x, pattern, imgurls