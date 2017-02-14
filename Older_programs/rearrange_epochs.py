import os


blazar_name = "RBPLJ1558+5628"

blazar = os.path.join("/home/siddharth/Desktop/",blazar) 

a = os.listdir(blazar)

os.chdir(blazar)

for nights in a:
    os.chdir(nights)
    

