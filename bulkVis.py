# -*- coding: utf-8 -*-
# clustering code:
# 3D simulation with projected images on cube faces

#some libraries
import numpy as np
import math
import sys
import time
import curses

#############
### curse display
#############

def report_hits(arr):
    offsetX=0
    for a in arr:
        outStr="h:"+str(a)
        stdscr.addstr(0, offsetX, outStr,curses.color_pair(0))
        offsetX=offsetX+len(outStr)+1


def report_display(arr,face, event, topset=0):
    global cubeWidth
    #print to screen positions
    #stdscr.addstr(0, 0, SetMarkings(len(raceArr[0])))
    stdscr.addstr(0+topset, 0, "face {0} event {1}".format(face,event),curses.color_pair(0))
    offsetX=(face-1)%3*(cubeWidth*3+5)
    offsetY=5+int((face-1)/3)*(cubeWidth+5)
    for a in range(0,len(arr),1):
        #time.sleep(0.05)
        #stdscr.addstr(10+topset, 5, str(arr[a][2]),curses.color_pair(0))
        col=0
        if arr[a][2]>0:
            col=arr[a][2]
        stdscr.addstr(offsetY+arr[a][1]+topset, offsetX+arr[a][0]*3, "{:3d}".format(arr[a][2]),curses.color_pair(col))
    stdscr.refresh()
    #for a in range(0,len(arr),1):
        #stdscr.addstr(offsetY+arr[a][1], offsetX+arr[a][0]*3, "{:3d}".format(0),curses.color_pair(0))

#############
### NON-curse display
#############

def colStr(inStr,col):
    outStr="\x1b["+str(col)+"m"+inStr+"\x1b[0m"
    return outStr

def int2Colour(val,code, opt=""):
    
    if(type(val)==float):
        outStr=str("%3.0f" % val)
    else:
        outStr=str(str(val).zfill(3))
    
    if code>0:
        #print self
        #print np.log10(val)
        #print int(np.log10(val))
        if code<10:
            col=code+40
        else:
            col=code
        if "log" in opt or "Log" in opt:
            col=int(np.log10(code))+40
        outStr=colStr(outStr,col)
    
    #print outStr
    return outStr

#############
### array functions
#############

def GetFace(arr, side):
    global cubeWidth
    #number sides like a die
    #orientation x-y, z=0 on bottom=1, top=6
    #x-z, y=0 on left=2, right=5
    #y-z, x=0 in front=3, back=4
    face=[]
    if side>6 or side<1:
        print "GetFace: side problem {0}. Default to 1".format(side)

    for a in arr:
        if side==1 or side==6:
            if a[2]==0:
                face.append([a[0],a[1],a[3]])
        if side==2 or side==5:
            if a[1]==0:
                face.append([a[0],a[2],a[3]])
        if side==3 or side==4:
            if a[0]==0:
                face.append([a[1],a[2],a[3]])
    if len(face)>cubeWidth*cubeWidth or len(face)<cubeWidth*cubeWidth:
        print "face has dubious dimensions {0} ({1}):".format(len(face),cubeWidth*cubeWidth)

    return face

def attenuation(val,pos,face):
    global cubeWidth
    attFac=1
    if face<4 and face>0:
        att=(val-pos*attFac)
    elif face<7 and face>3:
        att=(val-(cubeWidth-pos)*attFac)
    else:
        att=-100
    return att


def ProjFace(arr, side):
    global cubeWidth
    attFac=1
    #number sides like a die
    #orientation x-y, z=0 on bottom=1, top=6
    #x-z, y=0 on left=2, right=5
    #y-z, x=0 in front=3, back=4
    #print "in ProjFace for side {0}".format(side)
    face=[]
    for a in range(0,cubeWidth,1):
        for b in range(0,cubeWidth,1):
            face.append([a,b,0])
    if side<1 or side>6:
        print "ProjFace: side problem {0}. Default to 1".format(side)
    
    #print "arr length:",len(arr)
    for a in arr:
        for f in face:
            if a[3]==0:
                continue
            if side==1 or side==6:
                if f[0]==a[0] and f[1]==a[1]:
                    f[2]=f[2]+attenuation(a[3],a[2],side)
                    #if f[2]>0:
                        #print "ProjFace(16): ",f
            if side==2 or side==5:
                if f[0]==a[0] and f[1]==a[2]:
                    f[2]=f[2]+attenuation(a[3],a[1],side)
                    #if f[2]>0:
                        #print "ProjFace(25): ",f
            if side==3 or side==4:
                if f[0]==a[1] and f[1]==a[2]:
                    f[2]=f[2]+attenuation(a[3],a[0],side)
                    #if f[2]>0:
                        #print "ProjFace(34): ",f
    if len(face)>cubeWidth*cubeWidth or len(face)<cubeWidth*cubeWidth:
        print "face has dubious dimensions {0} ({1}):".format(len(face),cubeWidth*cubeWidth)
    
    return face


def ShowArray(arr,arrEl=2,opt="off log"):
    
    global cubeWidth
    el=arrEl
    
    doDigi=False
    doCol=False
    if el>=len(arr[0]):
        print "specified element (",el,") beyond limit of array element:",len(arr[0]),". Using element 0."
        el=0
    elif el<0:
        print "-ve value --> binary fudge!"
        el=el*-1
        doDigi=True
    
    if "col" in opt or "Col" in opt:
        doCol=True
    
    row=0
    rowStr=""
    count=0
    for a in arr:
        #print "pos:",pos
        if count==cubeWidth:
            print rowStr
            count=0
            rowStr=""
        
        if doDigi==True:
            dig=0
            if(a[el]>cluTHL):
                dig=1
            val=dig
        
        if doCol==True:
            rowStr=rowStr+" "+int2Colour(a[2],a[2], opt)
        else:
            rowStr=rowStr+" "+str(val)
        
        count=count+1
    print rowStr #catch last row

#######################
########## Executive
#######################

cubeWidth= 10
delay=1.0
Nhits=3
Nevents=10
bulkArray=[]


#make voxels
for i in range(0,cubeWidth,1):
    for j in range(0,cubeWidth,1):
        for k in range(0,cubeWidth,1):
            bulkArray.append([j,i,k,0]) #x,y,c


#hits=[[1,2,3,10],[1,2,5,10],[3,2,5,10]]

#for b in bulkArray:
#    if b[3]>0:
#        print "occ(b):",b


def main(stdscr):

    #colours for display
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS,1):
        curses.init_pair(i+1, curses.COLOR_BLACK, i)

    for e in range(0,Nevents,1):

        #reset bulk array
        for b in bulkArray:
            if b[3]>0:
                b[3]=0

        #make new hits
        hits=[]
        for i in range(0,Nhits,1):
            hits.append([int(np.random.uniform(0,cubeWidth)),int(np.random.uniform(0,cubeWidth)),int(np.random.uniform(0,cubeWidth)),10])

        #load hits
        for b in bulkArray:
            for h in hits:
                if b[0]==h[0] and b[1]==h[1] and b[2]==h[2]:
                    #print "found voxel!",h
                    b[3]=h[3]

        #get faces
        faces=[]
        for f in range(1,7,1):
            tmpEl=ProjFace(bulkArray,f)
            faces.append(tmpEl)


        #show faces
        try:
            report_hits(hits)
            for f in range(1,4,1):
                report_display(faces[f-1],f,e,5)
                report_display(faces[f-1+3],f+3,e,5)
                #print "\n face {0}...".format(f)
                #ShowArray(faces[f-1],2,"col log")

        except curses.ERR:
            pass
        stdscr.getch()
        
        time.sleep(delay)
                 


stdscr = curses.initscr()
curses.wrapper(main)

exit()
