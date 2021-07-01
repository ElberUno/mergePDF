# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 13:14:05 2021

@author: Louis Beal
"""

import os

import numpy as np

def filegroup(inplist):
    
    raw = inplist
    
    # fill to max length
    lens = [len(x) for x in inplist]
    maxlen = max(lens)
    inplist = [list(x.ljust(maxlen," ")) for x in inplist]
    
    # create array for more efficent slicing
    arr = np.array(inplist)
    
    # build up from first letter, calculating number of unique strings
    # largest increase is flagged as cutoff point for grouping
    delt = []
    last = 0
    for n in range(1, maxlen):
        uniq = len(list(set(["".join(x) for x in arr[:,:n]])))
    
        if last == 0:
            last = uniq
    
        delta = uniq - last
        last = uniq
        
        delt.append(delta)
        
    cut_id = delt.index(max(delt))
    # print("cut at ", cut_id)
    
    # obtain longest-first sorted list of all unique roots
    cut = sorted(list(set(["".join(x).strip() for x in arr[:,:cut_id]])), key = len, reverse = True)
    
    grouped = {x:[] for x in cut}
    #attain membership via substring
    for string in raw:
        placed = False
        i = 0
        for substring in cut:
            
            if substring in string:
                placed = True
                grouped[substring].append(string)
                
                break
            
    #update singletons to full root
    convert = []
    for root in grouped:
            
        convert.append((root, os.path.commonprefix(grouped[root])))
    
    print(convert)
    
    complete = {}
    for pair in convert:
        old = pair[0]
        new = pair[1]
    
        complete[new] = grouped[old]
    
    return(complete)

if __name__ == "__main__":
    
    testlist = ["blah",
                "blah 1",
                "blah 2",
                "test",
                "test 2",
                "blag",
                "longtest",
                "testlong",
                "big boy test 1",
                "big boy test 2"]
    
    groups = filegroup(testlist)
    
    # print(groups)