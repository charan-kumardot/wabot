import glob
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
os.chdir(THIS_FOLDER)
myFiles = glob.glob('*.txt')
myFiles.sort()
mas=[]
for i in myFiles:
    with open(os.path.join(THIS_FOLDER, i),'rb') as f:
        mas.append(f.read())
 

Messages=[i for i in mas]    
count=len(Messages)