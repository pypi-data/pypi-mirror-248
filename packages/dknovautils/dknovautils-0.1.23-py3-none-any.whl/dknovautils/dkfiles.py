
from dknovautils.commons import *

import os
from os.path import join, getsize
import shutil
from pathlib import Path
from typing import Dict, Iterator, Set, Tuple

import hashlib

_debug = False

class DkFile(object):

    def __init__(self,pathstr) -> None:

        self.pathstr = pathstr

        self.path = Path(pathstr)


    @property
    def basename(self):
        return os.path.basename(self.path)
    
    @property
    def filesize(self):
        return getsize(self.path)
    
    @property
    def dirname(self):
        return os.path.dirname(self.path)
    
    def exists(self):
        return self.path.exists()
    
    def is_file(self):
        return self.path.is_file()
    
    def is_dir(self):
        return self.path.is_dir()    
    
    @staticmethod
    def file_md5(f:str,md5Cache:Dict[str,str]=None)->str:
        
        
        if md5Cache is None:
            md5Cache={}
            
        if f in md5Cache:
            r=md5Cache[f]
            assert len(r)==32
            return r
        else:
        
            iprint_debug(f'gen md5 {f}')
            bs = Path(f).read_bytes()
            md5 = hashlib.md5()
            # md5.update('how to use md5 in python hashlib?'.encode('utf-8'))
            md5.update(bs)
            r=md5.hexdigest().lower()
            assert len(r)==32
            
            md5Cache[f] = r
            return r    
        
        
    @staticmethod
    def listdir(d:str)->List:
        fs=[DkFile(join(d,f)) for f in os.listdir(d)]
        # fs=[DkFile(f) for f in fs]
        return fs
        
    @staticmethod
    def file_sha1(f:str)->str:
        import hashlib
        bs = Path(f).read_bytes()
        md5 = hashlib.sha1()
        # md5.update('how to use md5 in python hashlib?'.encode('utf-8'))
        md5.update(bs)
        r=md5.hexdigest().lower()
        assert len(r)==32
        return r     


class DkPyFiles(object):

    pass


if __name__=='__main__':
    
    print('OK')