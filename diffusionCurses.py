# -*- coding: utf-8 -*-
# test diffusion code:
# 1D diffusion based on constant

#some libraries
import numpy as np
import math
import sys
import time
import curses

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

def SetMarkings(num):
    #start/finish markings
    markStr="cells    :   "
    for r in range(0,num,1):
        if r<10:
            markStr=markStr+"-"+str(r)+"---"
        else:
            markStr=markStr+"-"+str(r)+"--"
    markStr=markStr+": finish"
    return markStr


def report_display(arr,org,offset=1):
    global delay
    #print to screen positions
    stdscr.addstr(offset, 0, SetMarkings(len(arr)))
    stdscr.addstr(offset+1, 0, "diffusion:  ",curses.color_pair(0))
    for a in range(0,len(arr),1):
        if a==origin:
            col=3
        elif arr[a]>0.5:
            col=4
        else:
            col=0
        stdscr.addstr("{:4.1f} ".format(arr[a]),curses.color_pair(col))
    stdscr.refresh()

def report_sum(arr,input):
    sum=0.0
    for d in range(0,len(arr),1):
        sum=sum+arr[d]
    col=0
    if abs(sum-input)>0.5:
        col=2
    stdscr.addstr(0, 0, "diffusion sum: {0}".format(sum),curses.color_pair(col))

#############
### line set-up
#############

length=21
offset=[5,5]
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


def main(stdscr):
    
    #colours for display
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS,1):
        curses.init_pair(i+1, curses.COLOR_BLACK, i)

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

        for d in range(0,len(diffArr),1):
            diffArr[d]=tempArr[d]
        report_sum(diffArr,input)
        report_display(diffArr,origin)
        time.sleep(delay)


stdscr = curses.initscr()
curses.wrapper(main)


exit()