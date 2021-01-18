import glob
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
os.chdir(THIS_FOLDER)
myFiles = glob.glob('*.txt')
myFiles.sort()

Messages=[open(os.path.join(THIS_FOLDER, i),'r').read() for i in myFiles]    
count=len(Messages)