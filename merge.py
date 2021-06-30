# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 15:39:36 2021

@author: Louis Beal
"""

import os
import glob

from fpdf import FPDF

class merge(FPDF):
    
    def load_images(self,folder):
        
        print("scanning in path")
        print(folder)
        
        self.files = glob.glob(folder + "*.jpeg")
    
        self.append_image()
    
    def append_image(self):
        
        for img in self.files:
            self.add_page()
            self.image(img,x=0,y=0,w=self.w,h=self.h)
    
    def save(self, path, name = "merged"):
        self.output(path + name + ".pdf")

class folderHandler:
    
    def __init__(self, folder):
        
        self._folder = folder.replace("/",r"\\")
        
        self._files = {}
        
        self.scan()
        self.identify()
        self.distinguish()

    @property
    def folder(self):
        return(self._folder)
    
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
        names = self._files["name"]
        
        maxlen = max([len(x) for x in names])
        
        print(names)
        
        for i in range(maxlen):
            this = [x.ljust(maxlen, " ")[i] for x in names]
            uniq = list(set(this))
            
            print(i, this)
        
        
    
if __name__ == "__main__":
    
    folder = r"./example/"
    
    test = folderHandler(folder)
    
    # print(test._files)