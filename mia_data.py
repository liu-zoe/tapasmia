#%% 
## Project Name: mia
### Program Name: mia_data.py
### Purpose: To load in data of MIA Collections. 
##### Date Created: Mar 2nd 2021
import requests
import pathlib
import os
import json
import pandas as pd
APP_PATH = str(pathlib.Path(__file__).parent.resolve())
ghurl='https://raw.githubusercontent.com/artsmia/collection'
#%%
# Read in github logins
f = open("github.txt", "r")
github_logins=f.read()
github_uname=github_logins.split(',')[0]
github_pw=github_logins.split(',')[1]
f.close()
#%%
# Set up github 
from github import Github
github = Github(github_uname, github_pw)
repo=github.get_repo("artsmia/collection")
del github_logins, github_uname, github_pw
#%%
# Download Department Folder
contents = repo.get_contents("departments")
for content_file in contents:
    filename=os.path.join(APP_PATH,'data',content_file.path)
    r = requests.get(ghurl+'/master/'+content_file.path)
    with open(filename, 'wb') as f:
        f.write(r.content)
f.close()
del f, r, filename, content_file
#%%
# Download Department Files
dep=dict()
for content_file in contents:
    filename=os.path.join(APP_PATH,'data',content_file.path)
    id=content_file.path.split('/')[1].replace('.json','')
    with open(filename) as f:
        data=json.load(f)
        name=data['name']
        dep[id]=data
f.close()
del content_file, contents, filename, id, f, data, name
#%%
# Download Objects Folder
contents = repo.get_contents("objects")
for content_file in contents[50:60]:           
    print(content_file.path)
    path=os.path.join(APP_PATH,'data',content_file.path)
    if not os.path.isdir(path):
        os.mkdir(path)
    for fold in repo.get_contents(content_file.path):
        filename=os.path.join(APP_PATH,'data',fold.path)
        r = requests.get(ghurl+'/master/'+fold.path)
        with open(filename, 'wb') as f:
            f.write(r.content)
f.close()
del f, r, filename, content_file
# %%
# Download Objects Files
obj=pd.DataFrame()#data frame for all objects
contents = repo.get_contents("objects")
for content_file in contents:
    foldname=content_file.path.split('/')[1]
    for fold in repo.get_contents(content_file.path):
        id=fold.path.split('/')[2].replace('.json','')
        filename=os.path.join(APP_PATH,'data',fold.path)
        try:
            with open(filename) as f: 
                j=json.load(f)
                d=pd.json_normalize(j)
                d['folder']=foldname
                d['obj_id']=id
                if len(obj)==0:
                    obj=d
                else:
                    obj=obj.append(d)
        except:
            print('[ERROR] ',fold.path)
del content_file, id, d, f, filename, j, fold, foldname
obj=obj.sort_values(by=['folder','obj_id'])
obj.to_csv(os.path.join(APP_PATH, 'data/objects.csv'),
        index=None, header=True)
