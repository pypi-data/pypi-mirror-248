"""
image signal processings
"""
import cv2
import random
import numpy as np
import math
import numpy as np
from skimage.filters import threshold_sauvola
import random

def random_augment_textlines(img):
    """random augment textline images
    step1: positional transforms:
        * random rotate
        * random pan
        * random squeeze
        * random smear
    step2: noises:
        * gaussian noise
        * salt and pepper noise
        * advanced salt and pepper noise
    textures (random trigger after each step):
        * blurs
        * down sample
        * jpg compression
        * binarize


    Args:
        img (_type_): input img

    Returns:
        _type_: _description_
    """
    # resize to 64 height
    img = cv2.resize(img,(int(img.shape[1]/img.shape[0]*64),64))
    # positional transforms
    if random.random()<0.5:
        img = rotate_img(img,angle=random.randint(-3,3),pad_color="WHITE")
    if random.random()<0.1:
        random_pan(img,color=255,h_pad=32,w_pad=100,crop=False)
    if random.random()<0.5:
        img = squeeze_image(img, squeeze_rate=3**random.uniform(-1,1))
    if random.random()<0.0:
        img = random_smear(img,n_time_factor=1)
    # noises
    if random.random()<0.5:
        img = additive_gaussian_noise(img, mean=0, var=10**random.uniform(-2,-1))
    if random.random()<0.1:
        img = salt_pepper_noise(img, s_vs_p=0.5, freq=10**random.uniform(-3,-2))
    if random.random()<0.1:
        img = advanced_salt_pepper(img,size=10)
    
    # textures
    if random.random()<0.5:
        img = blur_image(img,blur_type=random.choice(["gaussian","median","bilateral","box"]),intensity=random.choice([3,5]))
    if random.random()<0.5:
        img = down_sample(img,down_sample_rate=3**random.uniform(-1,0.5),nearest=False)
    if random.random()<0.1:
        img = binarize_img(img,mode=random.choice(["threshold","otsu","sauvola"]),thresh=random.randint(0,255))
    if random.random()<0.5:
        img = jpg_artifact(img, quality=random.randint(30,80))
    return img


# blurs
def blur_image(img,blur_type="gaussian",intensity=3):
    """randomly blur image

    Args:
        img (_type_): _description_
        blur_type (str, optional): _description_. Defaults to "gaussian".
        blur_range (tuple, optional): _description_. Defaults to (1,5).

    Returns:
        _type_: _description_
    """
    if blur_type == "gaussian":
        img = cv2.GaussianBlur(img,(intensity,intensity),0)
    elif blur_type == "median":
        img = cv2.medianBlur(img,intensity)
    elif blur_type == "bilateral":
        img = cv2.bilateralFilter(img,intensity,75,75)
    elif blur_type == "box":
        img = cv2.blur(img,(intensity,intensity))
    return img

# random squeeze and stretch, length wise
def squeeze_image(img, squeeze_rate=0.5):
    """randomly squeeze image, length wise
       h*w image will be squeezed to (h/squeeze_rate) * w if squeeze_rate < 1
       h*w image will be squeezed to h * (w*squeeze_rate) if squeeze_rate > 1

    Args:
        img (_type_): input img
        squeeze_rate (float, optional): 
            squeeze rate, smaller is thinner. larger is fatter, Defaults to 0.5.
    """
    h, w = img.shape[:2]
    if squeeze_rate < 1:
        img = cv2.resize(img, (w, int(h / squeeze_rate)))
    else:
        img = cv2.resize(img, (int(w * squeeze_rate), h))
    return img


def down_sample(img,down_sample_rate=0.5,nearest=False):
    """down sample and up sample image, to simulate low resolution

    Args:
        img (_type_): _description_
        down_sample_rate (float, optional): _description_. Defaults to 0.5.

    Returns:
        _type_: _description_
    """
    h,w = img.shape[:2]
    img = cv2.resize(img,(int(img.shape[1]*down_sample_rate),int(img.shape[0]*down_sample_rate)))
    if nearest:
        img = cv2.resize(img,(w,h),interpolation=cv2.INTER_NEAREST)
    else:
        img = cv2.resize(img,(w,h))
    return img

# thresh
def binarize_img(img,mode="otsu",thresh=128):
    if len(img.shape)>2:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    if mode == "threshold":
        img = np.array(img > thresh, dtype=np.uint8)
    elif mode == "otsu":
        _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    elif mode == "sauvola":
        thresh_sauvola = threshold_sauvola(img, window_size=25)
        binary_sauvola = img > thresh_sauvola
        return np.array(binary_sauvola*255,dtype=np.uint8)
        
    return img

def advanced_salt_pepper(img,size=10):
    h,w = img.shape[:2]
    max_edge = max(h,w)
    pepper_map = np.array(255*(gen_cloud_noise(h=max_edge,w=max_edge,r=size)<0.7),dtype=np.uint8)
    pepper_map = pepper_map[:h,:w]
    pepper_map = cv2.cvtColor(pepper_map,cv2.COLOR_GRAY2BGR)
    pepper_map = cv2.blur(pepper_map, (3, 3))
    salt_map = np.array(255-255*(gen_cloud_noise(h=max_edge,w=max_edge,r=size)<0.7),dtype=np.uint8)
    salt_map = salt_map[:h,:w]
    salt_map = cv2.cvtColor(salt_map,cv2.COLOR_GRAY2BGR)
    salt_map = cv2.blur(salt_map, (3, 3))
    img = np.minimum(pepper_map,img)
    img = np.maximum(salt_map,img)

    return img

import numpy as np
import os
import cv2


def additive_gaussian_noise(img, mean=0, var=0.1):
    h, w = img.shape[:2]
    c = 0
    if len(img.shape) == 3:
        c = img.shape[2]

    sigma = var ** 0.5
    if c > 0:
        gauss_noise = np.random.normal(mean, sigma, (h, w, c))
    else:
        gauss_noise = np.random.normal(mean, sigma, (h, w))
    img = np.clip(img * (1 + gauss_noise), 0, 255)
    img = np.array(img, dtype=np.uint8)
    return img


def salt_pepper_noise(img, s_vs_p=0.5, freq=0.005):
    h, w = img.shape[:2]

    num_salt = np.ceil(freq * h * w * s_vs_p)
    num_pepper = np.ceil(freq * h * w * s_vs_p)
    salt_coords = [np.random.randint(0, i - 1, int(num_salt))
                   for i in img.shape]
    pepper_coords = [np.random.randint(0, i - 1, int(num_pepper))
                     for i in img.shape]
    img[tuple(salt_coords)] = 255
    img[tuple(pepper_coords)] = 0

    return img


def poisson_noise(img):
    vals = len(np.unique(img))
    vals = 2 ** np.ceil(np.log2(vals))
    noisy = np.random.poisson(img * vals) / float(vals)
    noisy = np.clip(noisy, 0, 255)
    noisy = np.array(noisy, dtype=np.uint8)
    return noisy


def dead_fly_noise(img, mode="pepper", grain_freq=0.005, grain_size=50):
    # grain size: 1x to 2x of char size
    if len(img.shape) > 2:
        return NotImplementedError("no colored image for now")

    h, w = img.shape
    orig_h, orig_w = h, w
    blur_kernel = 3

    noise = np.random.rand(h, w) - 0.5
    #     noise = np.zeros((h,w))
    for i in range(max(1, int(np.log2(grain_size)))):
        noise += cv2.resize(np.random.rand(h, w), (orig_w, orig_h)) - 0.5
        noise /= 2
        h = h // 2
        w = w // 2
    noise += 0.5

    thresh = np.percentile(noise, grain_freq * 100)
    noise = cv2.blur(noise, (blur_kernel, blur_kernel))
    noise = (noise > thresh) * 255

    if mode == "pepper":
        img = np.minimum(img, noise)
    elif mode == "salt":
        img = np.maximum(img, 255 - noise)
    return img

# # noise
def gen_cloud_noise(h=1000,w=1000,r=10):
    orig_h, orig_w = h, w
    noise = np.random.rand(h, w) - 0.5
    #     noise = np.zeros((h,w))
    for i in range(max(1, int(np.log2(r)))):
        noise += cv2.resize(np.random.rand(h, w), (orig_w, orig_h)) - 0.5
        noise /= 2
        h = h // 2
        w = w // 2
    noise += 0.5
    return noise

def rotate_img(img, angle, pad_color):
    if pad_color == 'WHITE':
        pad_color = [255, 255, 255]
    if pad_color == 'BLACK':
        pad_color = [0, 0, 0]
    (h, w) = img.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    img = cv2.warpAffine(img, M, (nW, nH), borderValue=pad_color)
    return img

def random_pan(img,color=255,h_pad=100,w_pad=100,crop=False):
    top_pad = int(random.random()*h_pad*2)
    left_pad = int(random.random()*w_pad*2)
    img = np.pad(img,[[top_pad,h_pad*2-top_pad],[left_pad,w_pad*2-left_pad],[0,0]],
                 mode='constant',constant_values=255)
    if crop:
        img = img[h_pad:-h_pad,w_pad:-w_pad]
    return img


def jpg_artifact(img, quality=40):
    """ compress image and reload to give image compress aritfact

    Args:
        img (_type_): _description_
        jpg_compress_rate (_type_): _description_

    Returns:
        _type_: _description_
    """
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    _, encimg = cv2.imencode('.jpg', img, encode_param)
    img = cv2.imdecode(encimg, 0)
    return img


def random_smear(img,n_time_factor=1):
    radius = 20
    h,w = img.shape[:2]
    img_warp = img.copy()
    n_times = int(max(1,(w/radius-2))*max(1,(h/radius-2))/4*n_time_factor)
    n_times = max(1,n_times)
    n_time = min(50,n_times)
    for i in range(n_times):
        try:
            x1 = random.randint(radius,w-radius-1)
            y1 = random.randint(radius,h-radius-1)
            x2 = random.randint(max(radius,x1-radius),min(w-radius-1,x1+radius))
            y2 = random.randint(max(radius,y1-radius),min(h-radius-1,y1+radius))
            # print(x1,y1,x2,y2,radius)
            img_warp = _localTranslationWarp(img_warp, x1,y1,x2,y2,radius)
        except:
            pass
    return img_warp

def _localTranslationWarp(srcImg, startX, startY, endX, endY, radius):
    ddradius = float(radius * radius)
    copyImg = np.zeros(srcImg.shape, np.uint8)
    copyImg = srcImg.copy()
    # 计算公式中的|m-c|^2
    ddmc = (endX - startX) * (endX - startX) + (endY - startY) * (endY - startY)
    H, W, C = srcImg.shape
    # print(srcImg.shape)
    for i in range(W):
        for j in range(H):
            # 计算该点是否在形变圆的范围之内
            # 优化，第一步，直接判断是会在（startX,startY)的矩阵框中
            if math.fabs(i - startX) > radius and math.fabs(j - startY) > radius:
                continue
            distance = (i - startX) * (i - startX) + (j - startY) * (j - startY)
            if (distance < ddradius):
                # 计算出（i,j）坐标的原坐标
                # 计算公式中右边平方号里的部分
                ratio = (ddradius - distance) / (ddradius - distance + ddmc)
                ratio = ratio * ratio
                # 映射原位置(向后变形，j后+变-即为向前变形)
                UX = i + ratio * (endX - startX)
                UY = j + ratio * (endY - startY)
                # 根据双线性插值法得到UX，UY的值
                value = _bilinear_insert(srcImg, UX, UY)
                # 改变当前 i ，j的值
                copyImg[j, i] = value
    return copyImg

"""
bilinearInsert:双线性插值法（变换像素）
"""
def _bilinear_insert(src, ux, uy):
    w, h, c = src.shape
    if c == 3:
        x1 = int(ux)
        x2 = x1 + 1
        y1 = int(uy)
        y2 = y1 + 1
        part1 = src[y1, x1].astype(np.float) * (float(x2) - ux) * (float(y2) - uy)
        part2 = src[y1, x2].astype(np.float) * (ux - float(x1)) * (float(y2) - uy)
        part3 = src[y2, x1].astype(np.float) * (float(x2) - ux) * (uy - float(y1))
        part4 = src[y2, x2].astype(np.float) * (ux - float(x1)) * (uy - float(y1))
        insertValue = part1 + part2 + part3 + part4
        return insertValue.astype(np.int8)
        
