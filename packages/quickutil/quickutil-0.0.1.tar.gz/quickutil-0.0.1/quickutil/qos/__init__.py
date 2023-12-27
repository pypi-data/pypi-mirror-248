import os
import shutil
from . import qdir

class qfile:
    def __init__(self,file_dir):
        self.dir = file_dir

    def get(self):
        return self.dir

    def change(self,new_dir):
        self.dir = new_dir

    def read(self, n = None):
        with open(self.dir,"r") as file:
            return file.read(n)

    def write(self, text):
        with open(self.dir,"w") as file:
            file.write(text)

    def append(self, text):
        with open(self.dir,"a") as file:
            file.write(text)

    def writelines(self,lines):
        with open(self.dir,"w") as file:
            file.writelines(lines)

    def create(self):
        if not os.path.exists(self.dir):
            open(self.dir,"x").close()

    def rename(self,new_name):
        os.rename(self.dir, new_name)

    def remove(self):
        os.remove(self.dir)

    def move(self, new_path):
        shutil.move(self.dir,new_path)

    def copy(self,dst,copyfunction=shutil.copy):
        copyfunction(self.dir,dst)

    def exists(self):
        return os.path.exists(self.exists())