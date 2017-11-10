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

def markingStr(offset,Nplanes,Zdist):

    markStr=""
    markStr=markStr+offset+"p0"
    for p in range(1,Nplanes,1):
        for z in range(0,Zdist,1):
            markStr=markStr+"-"
        markStr=markStr+"p"+str(p)

    return markStr

def report_maps(arr,dist,num=-1):
    #print to maps
    global mapPos
    global NpixPerPlane
    mark="maps:"
    if num>-1:
        mark="maps({:1d}):".format(num)
    markStr=markingStr(mark,len(arr),dist+5)
    stdscr.addstr(0, 0, markStr,curses.color_pair(0))
    map=0
    for a in arr:
        for b in range(0,len(a),1):
            col=0
            if a[b]>0:
                col=a[b]+1
            row=int(b/NpixPerPlane)
            column=b%NpixPerPlane
            stdscr.addstr(row+1, 8+ column*2+ map*(dist+7), str(a[b]),curses.color_pair(col))
        map=map+1

    stdscr.refresh()

def projectMap(arr,width,axis=1):

    proj=[]
    for w in range(0,width,1):
        proj.append(0)
    for a in range(0,len(arr),1):
        if arr[a]>0:
            if axis==1:
                proj[a%width]=proj[a%width]+arr[a]
            if axis==2:
                proj[int(a/width)]=proj[int(a/width)]+arr[a]
    return proj


def report_planes(arr,dist,num=-1):
    #print to plane positions
    global planePosX
    global planePosY
    planePos=planePosX
    planeStr="planesX"
    if num<0:
        planePos=planePosY
        planeStr="planesY"
    mark=planeStr+"({:1d}):".format(num)
    if(num<0):
        mark=planeStr+"({:1d}):".format(-num)
    markStr=markingStr(mark,len(arr),dist)
    stdscr.addstr(planePos, 0, markStr,curses.color_pair(0))
    pNum=0
    for a in arr:
        pxNum=0
        for b in a:
            col=0
            if b>0:
                col=b+1
            stdscr.addstr(planePos+1+pxNum, 11+ pNum*(dist+2), str(b),curses.color_pair(col))
            pxNum=pxNum+1
        pNum=pNum+1

    stdscr.refresh()

#############
### settings functions
#############

def showParams():
    global params
    print "Settings... name,value,description"
    count=1
    for p in params:
        outStr=str(count)+": "+p[0]+"="+str(p[2])+", "+p[1]
        print outStr
        count=count+1

def getParam(name):
    global params
    for p in params:
        if p[0]==name:
            return p[2]
    return -1

def setParam(num,val):
    global params
    params[num-1][2]=val

#######################
########## Executive
#######################

#set parametes
params=[] #array of triples: name,description,value

params.append(["Nplanes","number of planes",6])
params.append(["NpixPerPlane","(square) array size",10])
params.append(["Nevents","number of events",10])
params.append(["Zdist","plane separation (only used for plotting at the moment)",5])
params.append(["Ntracks","number of tracks per event (not implemented yet)",1])
params.append(["NnoisePerPlane","maximum number of noisy pixels per plane per event (then 50% chance)",1])
#random placing of noisy channel
params.append(["delay","delay between events for plotting",0.5])
params.append(["scatProb","probability of not scattering per plane (0,1). X/Y treated independently",0.8])
params.append(["incidenceX","X position of incident tracks (-1 for random)",-1])
params.append(["incidenceY","Y position of incident tracks (-1 for random)",-1])
#random direction in dimension of scatter +/-1

proceed=False
while proceed==False:
    showParams()
    optIn=raw_input("choose a number to set value or press enter to continue: ")
    try:
        opt = int(optIn)
        if opt>-1 and opt<len(params):
            valIn=float(raw_input("enter value: "))
            try:
                val = float(valIn)
                setParam(opt,val)
            except:
                print "Not a valid number. Reset defaults"
                proceed=False
        else:
            proceed=True
    except:
        print "Not a valid number. Continue with defaults."
        proceed=True

print "Final settings..."
showParams()
time.sleep(1)
print "Ready to run..."
time.sleep(1)

#access parameters by params array functions

infoPos=0 # veritical position of event infromation (not used at the moment)
mapPos=2 # veritical position of map plots
planePosX=15 # veritical position of X projections
planePosY=30 # veritical position of Y projections


Nplanes=int(getParam("Nplanes"))
NpixPerPlane=int(getParam("NpixPerPlane"))

planeArr=[]

#make planes
for p in range(0,Nplanes,1):
    plane=[]
    for q in range(0,NpixPerPlane*NpixPerPlane,1):
        plane.append(0)
    planeArr.append(plane)


def main(stdscr):

    #colours for display
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS,1):
        curses.init_pair(i+1, curses.COLOR_BLACK, i)

    #get parameters
    Ntracks=int(getParam("Ntracks"))
    scatProb=getParam("scatProb")
    NnoisePerPlane=int(getParam("NnoisePerPlane"))
    delay=getParam("delay")
    Nevents=int(getParam("Nevents"))
    Zdist=int(getParam("Zdist"))
    incidenceX=int(getParam("incidenceX"))
    incidenceY=int(getParam("incidenceY"))

    #run event loop
    try:
        for r in range(0,Nevents,1):
            
            #clear planes for new track
            for p in range(0,Nplanes,1):
                for q in range(0,NpixPerPlane*NpixPerPlane,1):
                    if planeArr[p][q]>0:
                        planeArr[p][q]=0
        
            #make track hits
            #make this vector of hits from gradient later
            track=[]
            if incidenceX==-1:
                incX=int(np.random.uniform(0,NpixPerPlane))
            else:
                incX=incidenceX
            if incidenceY==-1:
                incY=int(np.random.uniform(0,NpixPerPlane))
            else:
                incY=incidenceY
            track=[incY*NpixPerPlane+incX]
            for i in range(1,Nplanes,1):
                pos=track[i-1]
                spin=np.random.uniform(0,1) #up/down scatter
                if(spin>scatProb): #decide to scatter
                    updown=np.random.uniform(0,1)
                    if(updown>0.5) and track[i-1]+NpixPerPlane<NpixPerPlane*NpixPerPlane: #scatter direction
                        pos=pos+NpixPerPlane
                    elif (updown<=0.5) and track[i-1]-NpixPerPlane>-1:
                        pos=pos-NpixPerPlane
                    else:
                        pos=pos
                else:
                    pos=track[i-1]
                spin=np.random.uniform(0,1) #left/right scatter
                if(spin>scatProb): #decide to scatter
                    leftright=np.random.uniform(0,1)
                    if(leftright>0.5) and track[i-1]+1<NpixPerPlane*NpixPerPlane: #scatter direction
                        pos=pos+1
                    elif (leftright<=0.5) and track[i-1]-1>-1:
                        pos=pos-1
                    else:
                        pos=pos
                else:
                    pos=pos
                track.append(pos)
            
        
            #add track hits
            for p in range(0,Nplanes,1):
                planeArr[p][track[p]]=5
            
                #noise on plane
                for n in range(0,NnoisePerPlane,1):
                    spin=np.random.uniform(0,1)
                    if(spin>0.5):
                        px=int(np.random.uniform(0,NpixPerPlane))*NpixPerPlane+int(np.random.uniform(0,NpixPerPlane))
                        planeArr[p][px]=planeArr[p][px]+1
            
            projXArr=[]
            projYArr=[]
            for p in planeArr:
                projXArr.append(projectMap(p,NpixPerPlane,1))
                projYArr.append(projectMap(p,NpixPerPlane,2))
            
            report_maps(planeArr,NpixPerPlane+Zdist,r)
            report_planes(projXArr,Zdist,r)
            report_planes(projYArr,Zdist,-r)
            time.sleep(delay)

    except curses.ERR:
        pass
    stdscr.getch()
                 


stdscr = curses.initscr()
curses.wrapper(main)

exit()
