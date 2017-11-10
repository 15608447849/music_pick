
import json
import sys,os
from src.Entry.JsonBean import MusicBean

#json支持 : None, bool, int, float, string, list, tuple, dict.

def object2json(jsonObj):
    jsonStr = json.dumps(jsonObj.__dict__)
    print(jsonStr)
def object2jsonAndToFile(jsonObj,path):
    with open(path, 'w') as file:
        json.dump(jsonObj.__dict__, file)

def list2jsonAndToFile(list,path):
    with open(path, 'w') as file:
        json.dump(list, file)

def string2JsonBean(jsonStr):
    return json.loads(jsonStr)



