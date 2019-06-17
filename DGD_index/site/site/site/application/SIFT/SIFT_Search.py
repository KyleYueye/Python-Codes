# import cv
import cv2
import numpy as np
import math
import os
import json
from application.SIFT.pHash_Compare import filtrate

corner_number = 30


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
        vectors.append(vector)
    return vectors


def getPyramid(img):
    y_size, x_size = img.shape[:2]
    imglist = []
    imglist.append(cv2.resize(img, (x_size << 1, y_size << 1)))
    for i in range(3):
        imglist.append(cv2.resize(img, (x_size >> i, y_size >> i)))
    return imglist


def getChar(imglist):
    corners = []
    grads = []
    for i in imglist:
        g = cv2.goodFeaturesToTrack(i,
                                    maxCorners=corner_number,
                                    qualityLevel=0.01,
                                    minDistance=10,
                                    blockSize=3,
                                    k=0.04)
        corners.append(g[:, 0, :].astype(np.int))
    addEdge(imglist, corners)
    for i in imglist:
        grads.append(getGrad(i))
    main_directs = getMainDirect(grads, corners)
    vectors = getVectors(grads, main_directs)
    return vectors, main_directs


def getTargetChar(img):
    imglist = getPyramid(img)
    chars, corners = getChar(imglist)
    return chars, corners


def getmin2dis2(target, rvector):
    tmp = np.zeros(target.shape[0]).reshape(-1, 1)
    resource = rvector + tmp
    result = target - resource
    result *= result
    result = result.sum(axis=1)
    tmp = result.argmin()
    min1 = math.sqrt(result[tmp])
    result[tmp] = 10.0
    min2 = math.sqrt(result.min())
    return min1, min2


def getmin2dis_pos(target, rvector):
    tmp = np.zeros(target.shape[0]).reshape(-1, 1)
    resource = rvector + tmp
    result = target - resource
    result *= result
    result = result.sum(axis=1)
    pos = result.argmin()
    min1 = math.sqrt(result[pos])
    result[pos] = 10.0
    min2 = math.sqrt(result.min())
    return min1, min2, pos


def getMatchNumber(resources, target):
    match_numbers = np.zeros(len(resources), dtype="int")
    for i in range(len(resources)):
        for rvector in resources[i]:
            min1, min2 = getmin2dis2(target, rvector)
            if min1 < min2 * 0.75:
                match_numbers[i] += 1
    return match_numbers


def getBestMatch(resources, targets, res_num):
    match_numbers = np.zeros([len(targets), len(resources)], dtype="int")
    for i in range(len(targets)):
        match_numbers[i] = getMatchNumber(resources, targets[i])

    rn = []
    for i in range(res_num):
        tmp = match_numbers.argmax()
        rn.append(tmp % len(resources))
        match_numbers[:, tmp % len(resources)] = 0
    return rn


def search(img, r_chars, f_list, file_list, hash_list, res_num=10):
    scope = filtrate(img, file_list, hash_list)
    resource_chars = []
    file_list = []
    for i in range(len(r_chars)):
        if f_list[i] in scope:
            resource_chars.append(r_chars[i])
            file_list.append(f_list[i])
    target_chars, target_corners = getTargetChar(img)
    match = getBestMatch(resource_chars, target_chars, res_num)

    result = []
    for i in match:
        result.append(file_list[i])
    return result
