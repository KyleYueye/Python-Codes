import cv2
import numpy as np
import os
import collections
import json


def flatten(x):
    result = []
    for el in x:
        if isinstance(el, collections.Iterable) and not isinstance(el, str):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result


# print(flatten(["junk", ["nested stuff"], [], [[]]]))


def pHash(imgfile):
    """get image pHash value"""
    #加载并调整图片为32x32灰度图片
    img=cv2.imread(imgfile, 0)
    img=cv2.resize(img,(32,32),interpolation=cv2.INTER_CUBIC)

        #创建二维列表
    h, w = img.shape[:2]
    vis0 = np.zeros((h,w), np.float32)
    vis0[:h,:w] = img       #填充数据

    #二维Dct变换
    vis1 = cv2.dct(vis0)
    #cv.SaveImage('a.jpg',cv.fromarray(vis0)) #保存图片
    vis1.resize(8,8)

    #把二维list变成一维list
    img_list=flatten(vis1.tolist())

    #计算均值
    avg = sum(img_list)*1./len(img_list)
    avg_list = ['0' if i<avg else '1' for i in img_list]

    #得到哈希值
    return ''.join(['%x' % int(''.join(avg_list[x:x+4]),2) for x in range(0,8*8,4)])



def dump_json(file_list,hash_list):
    with open("hash_file.json", "w") as f:
        json.dump(file_list, f)
    with open("hash_hash.json", "w") as f:
        json.dump(hash_list, f)


if __name__ == '__main__':
    # s_t = pHash("target.jpg")
    # s_r = []
    # for root, dirctnames, filenames in os.walk("dataset"):
    #     for i in filenames:
    #         try:
    #             s_r = pHash(os.path.join(root, i))
    #             print(hammingDist(s_t,s_r),i)
    #         except:
    #             pass
    dir = "thepaper"
    files = os.listdir(dir)
    file_list = []
    hash_list = []
    for file in files:
        try:
            hash_list.append(pHash(os.path.join(dir,file)))
            file_list.append(os.path.join(dir,file))
        except:
            pass

    dump_json(file_list,hash_list)
