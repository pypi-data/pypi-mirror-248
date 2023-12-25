from glob import glob
from os.path import join
import json
from pprint import pprint
import cv2
import numpy as np
import re
from src.ht2.utils_dev.converts import points_to_cnt
from src.ht2.utils_dev.text import clean_up_english_spaces

def cut_segments_from_img(img,cnts):
    """cut segments from image

    Args:
        img (np.array): image
        cnts (list): list of cnts
    Returns:
        list: list of segment images
    """
    segment_imgs = []
    for cnt in cnts:
        mask = np.zeros_like(img)
        cv2.drawContours(mask,[cnt],0,(255,255,255),-1)

        bbox = cv2.boundingRect(cnt)
        segment_img = img[bbox[1]:bbox[1]+bbox[3],bbox[0]:bbox[0]+bbox[2]]
        mask = mask[bbox[1]:bbox[1]+bbox[3],bbox[0]:bbox[0]+bbox[2]]
        background_color = np.median(segment_img[mask == 0])
        if np.isnan(background_color):
            background_color = 255
        segment_img = np.maximum(255-mask,segment_img)
        segment_img = np.minimum(np.array(np.ones_like(segment_img)*background_color,dtype=np.uint8),segment_img)
        segment_imgs.append(segment_img)
    return segment_imgs


def clean_latex_eng_label(label):
    """remove \\quad
       make sure only one space between words
       make sure only one space after punctuations
       make sure no space before punctuations
       \\insert{xxx} -> xxx

    Args:
        label (_type_): _description_
    """
    label = label.replace("\\quad"," ")
    label = label.replace("\\deletion"," ")
    label = label.replace("\\del"," ")
    label = label.replace("\\insert{"," ")
    label = label.replace("}"," ")

    

    label = clean_up_english_spaces(label)
    return label

def parse_transcription_label_1(img,label):
    """parse label json from labeling platfrom into list of dicts
       of cleaned ones

    Args:
        label (dict): _description_
    Returns:
        list: [{"img":segment_imgs, "text":egment_labels}]
    """
    segment_labels = [] # {"cnt","text"}
    h,w = img.shape[:2]
    for segment in label["result"]["data"]:
        cnt = points_to_cnt(segment["points"],h,w)
        text = segment["text"]
        segment_labels.append({"cnt":cnt,"text":text})
    segment_imgs = cut_segments_from_img(img,[x["cnt"] for x in segment_labels])
    return [{"img":segment_imgs[i],
             "text":clean_latex_eng_label(segment_labels[i]["text"])} for i in range(len(segment_labels))]
        
import jiwer
import editdistance

def compare_text_results(path,label_ext,pred_ext,ignore_case = True,ignore_punc=True):
    """compare text results from two different sources,
       sources are in the same folder with different exts,
       example: 
            path = "/data/ht2/ocr_results", label_ext = "_label", pred_ext = "_pred"
        labels are /data/ht2/ocr_results/xxx_label.txt
        preds are /data/ht2/ocr_results/xxx_pred.txt
        calculate WER, CER save into list of dicts 

    Args:
        path (str): path to folder
        label_ext (str): ext for label
        pred_ext (str): ext for pred
    Returns:
        list: list of dicts like
        {"label_path":label_path,
         "pred_path":pred_path,
         "label":label,
         "label_len":label_len,
         "label_word_len":label_word_len,
         "pred":pred,
         "wer":wer,
         "cer":cer}
        }
    """
    label_paths = glob(join(path,"*"+label_ext+".txt"))
    pred_paths = glob(join(path,"*"+pred_ext+".txt"))
    label_paths.sort()
    pred_paths.sort()
    assert len(label_paths) == len(pred_paths)
    results = []
    for label_path,pred_path in zip(label_paths,pred_paths):
        with open(label_path,"r") as f:
            label = f.read()
        with open(pred_path,"r") as f:
            pred = f.read()
        label_len = len(label)            
        label_word_len = len(label.split(" "))
        if not label or not label.replace(" ",""):
            wer = 0
            cer = 0
        elif not pred:
            wer = 1
            cer = 1
        else:
            label_eval = label
            pred_eval = pred
            if ignore_case:
                label_eval = label_eval.lower()
                pred_eval = pred_eval.lower()
            if ignore_punc:
                label_eval = label_eval.replace(".","")
                label_eval = label_eval.replace(",","")
                label_eval = label_eval.replace("。","")
                pred_eval = pred_eval.replace("。","")
                pred_eval = pred_eval.replace(".","")
                pred_eval = pred_eval.replace(",","")
                

            wer = jiwer.wer(label_eval,pred_eval)
            cer = editdistance.eval(label_eval,pred_eval)/label_len
                
        results.append({"label_path":label_path,
                        "pred_path":pred_path,
                        "label":label,
                        "label_len":label_len,
                        "label_word_len":label_word_len,
                        "pred":pred,
                        "wer":wer,
                        "cer":cer})
    return results


    

