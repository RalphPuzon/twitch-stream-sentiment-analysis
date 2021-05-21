import os, glob
rootdir = os.getcwd() + "\\records\\"
dirnames = os.listdir(rootdir)
for direc in dirnames:
    path = rootdir + direc
    os.chdir(path)
    wfile = max(os.listdir('./'), key=os.path.getctime)
    print(wfile)

