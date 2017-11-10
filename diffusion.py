# -*- coding: utf-8 -*-
# test diffusion code:
# 1D diffusion based on constant

#some libraries
import numpy as np
import math
import sys
import time

#############
### functions
#############

def DiffuseVal(val1,val2,opt=-1):
    #return 1
    global diffConst
    diffVal=0.0
    if val1>val2:
        #diffVal=val1*diffConst
        diffVal=(val1-val2)*diffConst
    elif val2>val1:
        #diffVal=val2*diffConst
        diffVal=(val2-val1)*diffConst
    else:
        diffVal=0.0
    return diffVal

def strCol(inStr, code):
    if code>0:
        col=code%10 +40
        outStr="\x1b["+str(col)+"m"+inStr+"\x1b[0m"
    else:
        outStr=inStr
    #print outStr
    return outStr

def arr2str(arr):
    outStr=" "
    for a in arr:
        if a<0.005:
            outStr=outStr+"{:.2f} ".format(a)
        else:
            outStr=outStr+strCol("{:.2f} ".format(a),int(a))+" "
    return outStr


#############
### line set-up
#############

length=21
origin=10 #starting concentration position
diffConst=0.25 #rate of spread
input=100.0
delay=0.3
steps=100
print "diffuse!"

diffArr=[]
for l in range(0,length,1):
    diffArr.append(0.0)
diffArr[origin]=input

count=0

while count<steps:

    count=count+1
    
    tempArr=[]
    for l in range(0,length,1):
        tempArr.append(0.0)
            
    for d in range(0,origin+1,1):
        if diffArr[d]>0:
            #print "diffuse ",d,"..."
            #tempArr[d]=diffArr[d]
            if d-1>-1 and diffArr[d-1]<diffArr[d]:
                #print "spreading left(",d-1,"): ",diffArr[d-1],",",diffArr[d]
                tempArr[d-1]=tempArr[d-1]+DiffuseVal(diffArr[d-1],diffArr[d])
                if tempArr[d]>0.0:
                    tempArr[d]=tempArr[d]-DiffuseVal(diffArr[d-1],diffArr[d])
                else:
                    tempArr[d]=diffArr[d]-DiffuseVal(diffArr[d-1],diffArr[d])
            #print "done left: ",tempArr[d-1],",",tempArr[d]
            else:
                tempArr[d]=diffArr[d]


    for d in range(len(diffArr)-1,origin-1,-1):
        if diffArr[d]>0:
            #print "diffuse ",d,"..."
            #val=diffArr[d]
            #tempArr[d]=diffArr[d]
            if d+1<len(diffArr) and diffArr[d+1]<diffArr[d]:
                #print "spreading right(",d+1,"): ",diffArr[d],",",diffArr[d+1]
                tempArr[d+1]=tempArr[d+1]+DiffuseVal(diffArr[d],diffArr[d+1])
                if tempArr[d]>0.0:
                    tempArr[d]=tempArr[d]-DiffuseVal(diffArr[d],diffArr[d+1])
                else:
                    tempArr[d]=diffArr[d]-DiffuseVal(diffArr[d],diffArr[d+1])
            #print "done right: ",tempArr[d],",",tempArr[d+1]
            else:
                tempArr[d]=diffArr[d]
#tempArr[d]=val

    sum=0.0
    for d in range(0,len(diffArr),1):
        sum=sum+tempArr[d]
        diffArr[d]=tempArr[d]
    if abs(sum-input)>0.5:
        print "summation problem {0}>{1}".format(sum,input)
    sys.stdout.flush()
    sys.stdout.write('\r'+arr2str(diffArr))
    time.sleep(delay)
print '\n'
#print diffArr

exit()

