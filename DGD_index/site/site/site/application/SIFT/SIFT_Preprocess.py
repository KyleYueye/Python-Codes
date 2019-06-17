# import cv
import cv2
import numpy as np
import math
import time
import os
import json
import sys


def addEdge(imglist, corners):
    appdex_size = 80
    for i in range(len(imglist)):
        new_img = np.zeros((imglist[i].shape[0] + appdex_size, imglist[i].shape[1] + appdex_size), dtype="uint8")
        new_img[appdex_size // 2:-appdex_size // 2, appdex_size // 2:-appdex_size // 2] = imglist[i]
        imglist[i] = new_img
        corners[i] += appdex_size // 2


def getGrad(img):
    img = img.astype(np.int32)
    xdiff = img[1:-1, 2:] - img[1:-1, :-2]
    ydiff = img[2:, 1:-1] - img[:-2, 1:-1]
    grad = np.zeros([2, img.shape[0], img.shape[1]])
    grad[0, 1:-1, 1:-1] = np.sqrt(xdiff * xdiff + ydiff * ydiff)
    grad[1, 1:-1, 1:-1] = np.arctan2(ydiff, xdiff) - 0.0000000000001
    return grad


def GSmodel(zgm):
    size = int(round(3 * zgm) * 2 + 1)
    half = size / 2
    model = np.zeros((size, size))
    zgm = zgm * zgm
    for i in range(size):
        for j in range(size):
            model[i, j] = math.exp(-((half - i) * (half - i) + (half - j) * (half - j)) / 2 / zgm) / 2 / math.pi / zgm
    return model


def transDirects(grads, number):
    directs = []
    unit = np.pi * 2 / number
    for grad in grads:
        directs.append(((grad[1, ...] + np.pi) / unit).astype('int'))
    return directs


def transDirect(direct, number):
    unit = np.pi * 2 / number
    tmp = ((direct + np.pi) / unit).astype('int')
    return (tmp + 8) % 8


def getMainDirect(grads, corners):
    zgm = 1
    pillar_directs = transDirects(grads, 36)
    directs = []
    subscript = np.arange(36)
    gs = GSmodel(zgm)
    r = (gs.shape[0] - 1) // 2
    for i in range(len(grads)):
        directs.append([])
        for x0, y0 in corners[i]:

            wei_grad = grads[i][0, y0 - r:y0 + r + 1, x0 - r:x0 + r + 1] * gs
            direct = np.bincount(pillar_directs[i][y0 - r:y0 + r + 1, x0 - r:x0 + r + 1].ravel(), wei_grad.ravel(),
                                 minlength=36)
            grad_limit = direct.max() * 0.8
            for j in range(36):
                if direct[j] >= grad_limit:
                    directs[i].append((x0, y0, math.pi * (j - 18) / 18.0))
    return directs


def uniform(vector):
    length = math.sqrt((vector * vector).sum())
    return vector / length


def getVectors(grads, main_directs):
    vectors = []
    r = 10
    tmp1 = np.arange(-2 * r, 2 * r)
    tmp2 = np.zeros(4 * r).reshape(-1, 1)
    pos_in_corner = np.zeros((4 * r, 4 * r, 2))
    pos_in_corner[:, :, 0] = tmp1 + tmp2
    pos_in_corner[:, :, 1] = tmp1.reshape(-1, 1) + tmp2.reshape(1, -1)
    pos_in_img = np.zeros((4 * r, 4 * r, 2))
    tmp1 = (np.arange(4 * r) // r * 32).reshape(-1, 1)
    tmp2 = np.arange(4 * r) // r * 8
    appendex = tmp1 + tmp2
    for i in range(len(grads)):
        vector = np.zeros((len(main_directs[i]), 128))
        for j in range(len(main_directs[i])):
            pos_in_img[:, :, 0] = pos_in_corner[:, :, 0] * math.cos(main_directs[i][j][2]) - pos_in_corner[:, :,
                                                                                             1] * math.sin(
                main_directs[i][j][2]) + main_directs[i][j][0]
            pos_in_img[:, :, 1] = pos_in_corner[:, :, 0] * math.sin(main_directs[i][j][2]) + pos_in_corner[:, :,
                                                                                             1] * math.cos(
                main_directs[i][j][2]) + main_directs[i][j][1]
            tmp = np.round(pos_in_img).astype("int")
            grad = grads[i][:, tmp[:, :, 1], tmp[:, :, 0]]
            grad[1] = (grad[1] - main_directs[i][j][2] + np.pi) % (2 * np.pi) - np.pi
            transed = transDirect(grad[1], 8) + appendex
            vector[j] = uniform(np.bincount(transed.ravel(), grad[0].ravel(), minlength=128))
        vectors.append(vector.tolist())
    return vectors


def getPyramid(img):
    y_size, x_size = img.shape[:2]
    imglist = []
    imglist.append(cv2.resize(img, (x_size << 1, y_size << 1)))
    for i in range(3):
        imglist.append(cv2.resize(img, (x_size >> i, y_size >> i)))
    return imglist


def getChar(imglist):
    print(sys._getframe().f_code.co_name)
    corners = []
    grads = []
    print('Corner Points')
    for i in imglist:
        corners.append(
            cv2.goodFeaturesToTrack(i, maxCorners=corner_number, qualityLevel=0.01, minDistance=10, blockSize=3,
                                    k=0.04)[:, 0, :].astype("int"))
    print('Add Edge')
    addEdge(imglist, corners)
    print('Calc Grad')
    for i in imglist:
        grads.append(getGrad(i))
    print('Calc Dir')
    main_directs = getMainDirect(grads, corners)
    print('Calc Vec')
    vectors = getVectors(grads, main_directs)
    return vectors, main_directs


def readResourceImg(state=0):
    print(sys._getframe().f_code.co_name)
    imglist = []
    filelist = []
    for root, dirctnames, filenames in os.walk("thepaper"):
        for i in filenames:
            img = cv2.imread(os.path.join(root, i), state)
            try:
                if img == None:
                    continue
            except:
                pass
            imglist.append(img)
            filelist.append(os.path.join(root, i))
    return imglist, filelist


def getResourceChar():
    print(sys._getframe().f_code.co_name)
    imglist, filelist = readResourceImg()
    chars, corners = getChar(imglist)
    return chars, corners, filelist


def main():
    print(sys._getframe().f_code.co_name)
    resource_chars, resource_corners, filelist = getResourceChar()
    with open("sift_chars.json", "w") as f:
        json.dump(resource_chars, f)
    with open("sift_files.json", "w") as f:
        json.dump(filelist, f)


if __name__ == '__main__':
    # corner_number = int(input("please input max corner number:\n"))
    corner_number = 30
    main()
