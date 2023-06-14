import configparser
def read_config():
    config = configparser.ConfigParser()
    config.read('./configurations.ini')
    return config

from detection_helpers import Detector
#from tracking_helpers import *
#from bridge_wrapper import *
from PIL import Image

config=read_config()
#classes=bool(config['Detection']['classes'])
detector = Detector(classes=None) # it'll detect ONLY [person,horses,sports ball]. class = None means detect all classes. List info at: "data/coco.yaml"
detector.load_model('./weights/yolov7x.pt',) # pass the path to the trained weight file

import datetime
import os 
import cv2
#from IPython.core.interactiveshell import InteractiveShell
#InteractiveShell.ast_node_interactivity = "all" 

def create_file(path):
    if not os.path.exists(path):
        os.makedirs(path)
    #     print(f"{path} is created!")
    # else:
    #     print(f"{path} is existed")

def load_file_list(loadpath):
    filelist=[]
    for rootdir, _, files in os.walk(loadpath,topdown=False):
        if not loadpath==rootdir :
            files.sort(key=lambda x:int(x[:-4]))
            for subdir in rootdir.split(loadpath):
                if not subdir  == '':
                    filelist.append(loadpath+subdir)
    return filelist

#detectionloadpath=r'./capture_result/'
#detectionsavepath=r'./detection_result/'
config=read_config()
detectionloadpath=config['Detection']['detectionloadpath']
detectionsavepath=config['Detection']['detectionsavepath']

load_file_list(detectionloadpath)
create_file(detectionsavepath)

start=datetime.datetime.now()
for files in load_file_list(detectionloadpath):
    savetopath=files.replace(detectionloadpath,detectionsavepath)
    create_file(savetopath)
    fileslist=list(os.listdir(files))
    j=0
    print(' ')
    for file in fileslist:
        #print(files+'/'+file)
        result = detector.detect(files+'/'+file, plot_bb = True)
        if len(result.shape) == 3:# If it is image, convert it to proper image. detector will give "BGR" image
            result = Image.fromarray(cv2.cvtColor(result,cv2.COLOR_BGR2RGB)) 
            result.save(savetopath+'/'+file)
            j=j+1
            print(f"\r {savetopath}  處理進度 ： {j}/{len(fileslist)}",end="")
print('\n')
end=datetime.datetime.now()
print(f'總耗時: {(end-start)} ' )