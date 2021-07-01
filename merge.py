# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 15:39:36 2021

@author: Louis Beal
"""

import os
import re
import glob
import operator

import pandas as pd

from fpdf import FPDF

from filegroup import filegroup

class merge(FPDF):
    
    def create(self, folder, name, files):
        
        self.path = folder
        self.name = name
        
        self.files = files
        
        self.append_image()
    
    def append_image(self):
        
        for img in self.files:
            self.add_page()
            self.image(img,x=0,y=0,w=self.w,h=self.h)
    
    def save(self):
        outpath = self.path + self.name + ".pdf"
        
        print(f"\nsaving merged pdf at {outpath}")
        print("files contained:")
        for file in self.files:
            print(f"\t{file}")
        self.output(outpath)

class folderHandler:
    
    def __init__(self, folder):
        
        self._folder = folder.replace("/",r"\\")
        
        self._files = {}
        
        self._groups = False
        
        self.scan()
        self.identify()
        self.distinguish()
        self.sort()

    @property
    def folder(self):
        return(self._folder)
    
    @property
    def groups(self):
        
        if not self._groups:
            
            self.scan()
            self.identify()
            self.distinguish()
            self.sort()
            
        return(self._groups)
    
    def stripname(self, name):
    
        f = self.folder
        
        out = "".join(name.replace(f[:-1], "").split(".")[0:-1])
        ftype = name.split(".")[-1]
        
        return((out,ftype))
    
    def scan(self):
        # scan folder
        
        f = self.folder
        
        names = []
        
        ftypes = ("png", "jpg", "jpeg", "gif")
        
        for t in ftypes:
            names.extend(glob.glob(f + "*." + t))
        
        self._files["path"] = names
        self._files["name"] = [self.stripname(x)[0] for x in names]
        self._files["type"] = [self.stripname(x)[1] for x in names]
        
    def identify(self):
        
        #get file info for distinction
        
        names = self._files["path"]
        
        create = []
        modify = []
        for name in names:
            create.append(os.path.getctime(name))
            modify.append(os.path.getmtime(name))
            
        self._files["mod"] = modify
        self._files["crt"] = create
        
    def distinguish(self):
        
        #call the file grouper
        
        names = self._files["name"]
        
        groups = filegroup(names)
        
        self._groups = groups
        
    def sort(self):
        
        #sort files into order
        # first, try sort by numbers in the names, then by file dates
        groups = self._groups
        
        sort = {}
        for group in groups:
            files = groups[group]
            
            temp = []
            for file in files:
                nums = sum([int(x) for x in re.findall(r'-?\d+\.?\d*', file)])
                date = self.normtime(file)
                
                temp.append((file,nums,date))
                
            # sort by detected nums and then if not, create/modify date
            temp = [x[0] for x in sorted(temp, key = operator.itemgetter(1, 2))]
            
            #convert names back to paths
            paths = []
            for name in temp:
                paths.append(self._files["path"][self._files["name"].index(name)])
            
            sort[group] = paths
  
        self._groups = sort  
  
    def normtime(self, file):
        
        # return a value taking both create and modify times into account
        # sum should do the trick for now
        
        idx = self._files["name"].index(file)
        
        crt = self._files["crt"][idx]
        mod = self._files["mod"][idx]
        
        # print(f"norm time for {file}, {crt + mod}")
        
        return(crt + mod)
        
    
if __name__ == "__main__":
    
    folder = r"./example/"
    
    test = folderHandler(folder)
    
    groupings = test.groups
    
    for group in groupings:
        
        paths = groupings[group]
        
        temp = merge()
        
        temp.create(folder, group, paths)
        temp.save()