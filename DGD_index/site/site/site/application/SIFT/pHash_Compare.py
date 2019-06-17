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


def pHash(img):
    """get image pHash value"""
    # 加载并调整图片为32x32灰度图片

    img = cv2.resize(img, (32, 32), interpolation=cv2.INTER_CUBIC)

    # 创建二维列表
    h, w = img.shape[:2]
    vis0 = np.zeros((h, w), np.float32)
    vis0[:h, :w] = img  # 填充数据

    # 二维Dct变换
    vis1 = cv2.dct(vis0)
    # cv.SaveImage('a.jpg',cv.fromarray(vis0)) #保存图片
    vis1.resize(8, 8)

    # 把二维list变成一维list
    img_list = flatten(vis1.tolist())

    # 计算均值
    avg = sum(img_list) * 1. / len(img_list)
    avg_list = ['0' if i < avg else '1' for i in img_list]

    # 得到哈希值
    return ''.join(['%x' % int(''.join(avg_list[x:x + 4]), 2) for x in range(0, 8 * 8, 4)])


def hammingDist(s1, s2):
    dist = 0
    assert len(s1) == len(s2)
    for ch1, ch2 in zip(s1, s2):
        b1 = str(bin(int(ch1, 16)))[2:]
        b1 = b1.zfill(4)
        b2 = str(bin(int(ch2, 16)))[2:]
        b2 = b2.zfill(4)
        dist += sum([x != y for x, y in zip(b1, b2)])
    out_score = 1 - dist * 1. / (8 * 8)
    return out_score


def load_json():
    with open(os.path.join(os.getcwd(),  "hash_file.json"), "r") as f:
        file_list = json.load(f)
    with open(os.path.join(os.getcwd(),  "hash_hash.json"), "r") as f:
        hash_list = json.load(f)
    return file_list, hash_list


def filtrate(target, file_list, hash_list):
    s = pHash(target)
    imgs = []
    for i in range(len(file_list)):
        img = {}
        img["file"] = file_list[i]
        img["hash"] = hash_list[i]
        img["score"] = hammingDist(hash_list[i], s)
        imgs.append(img)
    imgs = sorted(imgs, key=lambda elem: elem["score"], reverse=True)
    res = [elem["file"] for elem in imgs]
    return set(res[:int(len(res) * 0.3)])


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
    f, h = load_json()
    print(filtrate(os.path.join(os.getcwd(),"thepaper", "httpsimage.thepaper.cnimage12828.jpg"),f,h))
