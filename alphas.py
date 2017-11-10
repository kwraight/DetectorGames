# -*- coding: utf-8 -*-
# clustering code:
# fill hit map with gaussians (pseudo-alphas)

import numpy as np
import clusteringClass as cc

#######################
########## Executive
#######################

cc.printBasic()

sensorArray=[]

cc.squareWidth = abs(int(raw_input("Square array size? ")))

for i in range(0,cc.squareWidth,1):
    for j in range(0,cc.squareWidth,1):
        sensorArray.append([j,i,0]) #x,y,c
cc.ShowArray(sensorArray,0,"")
#cc.printBasic()
raw_input("Array set-up. Press return to proceed...")

cc.occupancy= abs(int(raw_input("How many alphas? ")))

hits=cc.GetHits(cc.occupancy)
print "hits:",len(hits)
cc.AddHits(sensorArray,hits)
cc.ShowArray(sensorArray,2,"col log")
#cc.printBasic()
raw_input("Hits in array. Press return to proceed...")

cc.ApplyTHL(sensorArray,cc.cluTHL)
cc.ShowArray(sensorArray,2,"col log")
#cc.printBasic()
raw_input("THL applied. Press return to proceed...")


cluArr=cc.ClusterArray(sensorArray)
perArr=cc.CalcPerimeter(sensorArray,cluArr)

cc.UniArr(sensorArray,0)
count=0
for c in cluArr:
    count=count+1
    cc.AddColHits(sensorArray,c,count,"index")

cc.ShowArray(sensorArray,2,"col ")

circs=cc.Circularity(perArr,cluArr)

count=0
for c in cluArr:
    #print c
    count=count+1
    cc.ClusterParams(c,count+40)

for c in range(0,len(circs),1):
    print cc.colStr("circularity:",c+41),"{:.2f}".format(circs[c])

tPerps=[]
for p in perArr:
    tPerp=cc.TransverseAxis(p,"index")
    tPerps.append(tPerp)
    print "tPerp:",tPerp

cc.AddColHits(sensorArray,tPerps,45)

cc.ShowArray(sensorArray,2,"col ")


#cc.printBasic()
raw_input("Press return to exit")




exit()

