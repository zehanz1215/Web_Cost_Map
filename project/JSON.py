import os 
import json
import tqdm
import ast
import pandas as pd

cities=pd.read_excel('static/CostIndex.xlsx', header=0)
cityList=cities['city'].tolist()
cityListLower=[x.lower() for x in cityList if isinstance(x,str)]

# merge all the cities geojson into one geojson called sample.json:
def merge():
    res = {}
    for file in os.listdir("static/cities"):
        with open("static/cities/" + file, 'r', encoding="utf-8") as f:
            print(file)
            res[str(file)[:-5]] = json.load(f)
    fw = open("sample.json", "w")
    json.dump(res, fw)
    fw.close()

# merge all the cities geojson into one geojson called cities.json:
def mergeJson(pathRaw,pathResult):
    mergeFile=os.path.join(pathResult, 'cities.json')
    with open(mergeFile, 'w', encoding='utf-8') as f0:
        for file in os.listdir(pathRaw):
            with open(os.path.join(pathRaw,file),'r',encoding='utf-8') as f1:
                for line in tqdm.tqdm(f1):
                    line_dict=json.loads(line)
                    js=json.dumps(line_dict, ensure_ascii=False)
                    f0.write(js+'\n')
                f1.close()
        f0.close()

# add the material index, installation index, and average index to the us state geojson:
def addDataToJson():
    usState=pd.read_excel('static/usState.xlsx', header=0)
    with open('static/usstates.json','r') as f:
        loadF=json.load(f)
        features=loadF['features']
        n=len(features)
        for i in range(n):
            p=features[i]
            pro=p['properties']
            name=pro['NAME']
            index=usState[(usState.state==name)].index.tolist()
            if len(index)!=0:
                ave=usState.loc[index[0],'Average']
                material=usState.loc[index[0],'Material']
                install=usState.loc[index[0],'Installation']
                newList={'Material':material,'Installation':install,'Average':ave}
            else:
                newList={'Material':0,'Installation':0,'Average':0}
            pro.update(newList)
    with open("usstates.json","w") as f1:
        json.dump(loadF,f1)
        print("finish")
            
# find the geojson files which are from the cities we are focusing on, and
# merge those in one state to a specific geojson file:
def mergeCities():
    for folder in os.listdir("static/cities"):
        name=folder
        res={}
        for file in os.listdir("static/cities/" + folder):
            if str(file)[:-5] in cityListLower:
                with open("static/cities/"  +folder + '/' + file, 'r', encoding='utf-8') as f:
                    res[str(file)[:-5]] = json.load(f)
        fw = open("static/cities/" + name + '.json','w')
        json.dump(res, fw)
        fw.close()


# all functions in this python file only worked once.
if __name__=='__main__':
    # pathRaw,pathResult='./static/cities','./static'
    # if not os.path.exists(pathResult):
    #     os.mkdir(pathResult)
    # mergeJson(pathRaw,pathResult)
    # merge()
    # addDataToJson()
    # mergeCities()
    pass