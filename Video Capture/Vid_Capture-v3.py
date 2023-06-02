"""跳幀後再讀取,測試視頻使用了36秒"""
import os
import cv2
import datetime
import numpy as np 
from skimage.metrics import structural_similarity
import configparser

# Method to read config file settings
def read_config():
    config = configparser.ConfigParser()
    config.read('./configurations.ini')
    return config

def create_file(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print("The new directory is created!")

def video_path_list(VideoPath):
    video_path_list=[]
    for i in os.listdir(VideoPath):
        if i.endswith('.mp4'):
            video_path_list.append(os.path.join(VideoPath,i))
    return video_path_list

def video_name_list(VideoPath):
    video_name_list=[]
    for i in os.listdir(VideoPath):
        if i.endswith('.mp4'):
            video_name_list.append(i)
    return video_name_list

def create_each_video_file(vp,OutPutVideoPath):
    name=vp.split('\\')[-1]
    savepath=(OutPutVideoPath+'/'+name[:-4])
    create_file(savepath)
    print(f'儲存圖片的路徑：{savepath}')
    return savepath


def video_info(vp,FrameFrequency):
#cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # 攝像頭截取
    cap = cv2.VideoCapture(vp)
    #ret = cap.isOpened # 判斷是否成功打開
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # h
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # w
    dim =(width,height)
    print('寛度、高度分别为：',width,height) # 幀率 寛 高
    n_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print('總幀數：',n_frame) # 整个視頻的總幀數
    fps = cap.get(cv2.CAP_PROP_FPS) # 幀率 每秒展示多少張圖片
    print('幀速率：',int(fps))
    duration = n_frame/fps/60
    print(f'影片時長約： {round(duration,3)} 分鐘')        
    print(f'設定截取的幀速率為： {FrameFrequency}')
    print(f'預算截取圖片： {int((n_frame/FrameFrequency)-2)}  張') 
    return height,width,n_frame,fps,duration,dim

#InPutVideoPath = './video'
#FrameFrequency = 24 # 每frameFrequency保存一張圖片
#OutPutVideoPath = './result' # 設置保存路徑
#Similarity = 0.9

config=read_config()
InPutVideoPath=config['Settings']['InPutVideoPath']
OutPutVideoPath=config['Settings']['OutPutVideoPath']
FrameFrequency=eval(config['Settings']['FrameFrequency'])
Similarity=eval(config['Settings']['Similarity'])

print(f'InPutVideoPath : {InPutVideoPath}')
print(f'OutPutVideoPath: {OutPutVideoPath}')
print(f'FrameFrequency: {FrameFrequency}')
print(f'Similarity: {Similarity}')

create_file(OutPutVideoPath)
create_file(InPutVideoPath)
video_path_list(InPutVideoPath)
video_name_list(InPutVideoPath)

for vp in video_path_list(InPutVideoPath):
    print('     ')
    print('     ')
    print('----------------------------------------------------------------')
    print('start')
    print(f'正在轉換檔案{vp}')
    cap = cv2.VideoCapture(vp)
    ret = cap.isOpened # 判斷是否成功打開

    height,width,n_frame,fps,duration,dim= video_info(vp,FrameFrequency)
    savepath = create_each_video_file(vp,OutPutVideoPath)

    k = 0 # 多於兩張圖片時運行
    i=0
    count_in=[]
    count_out=[]
    img_files=[]
    spendtime=[]

    start=datetime.datetime.now()

    print('開始轉換')
    while ret: 
        now_fps = cap.get(1) 
        ret = cap.grab()
        #print(now_fps)
        if int(now_fps) == n_frame: # 结束标志是否读取到最后一幀
            break 
        if (now_fps % 24 == 0):
            #print(now_fps)
            i=i+1
            (flag,frame) = cap.read()
            fileName = str(int(i))+'.jpg'  
            img_files.append(frame)      
            k = k + 1
            if k > 1:
                img=img_files[-2]
                img1=img_files[-1]
                start2=datetime.datetime.now()
                #print(img.shape[0], img.shape[1])
                #print(dim)
                if (img.shape[0], img.shape[1]) != dim: 
                    img=cv2.resize(img ,dim, interpolation=cv2.INTER_AREA)    
                if (img1.shape[0], img1.shape[1]) != dim: 
                    img1=cv2.resize(img1 ,dim, interpolation=cv2.INTER_AREA) 
                ssim=structural_similarity(img, img1, channel_axis=-1,win_size=7)#channel_axis=-1,win_size=7
                end2=datetime.datetime.now()
                spendtime.append(end2-start2)
                #print(f'Running time: {end2-start2} ')
                if ssim < Similarity:
                    cv2.imwrite(savepath + '/' + fileName, img, [cv2.IMWRITE_JPEG_QUALITY,100])
                    #print(savepath + '/' + fileName , now_fps)
                    count_in.append(fileName)
                else:
                    count_out.append(fileName)
        print(f"\r處理進度： {round( ((now_fps+1) / n_frame )*100, 2)}%", end="")

    end=datetime.datetime.now()
    print('')
    print(f'已保留 {len(count_in)} 張圖片,刪除 {len(count_out)} 張圖片')
    print(f'圖片比對平均用時： {np.mean(spendtime)}')
    print(f'總耗時: {(end-start)} ' )
    print('end!')
    print('----------------------------------------------------------------')
    print('     ')
    print('     ')

