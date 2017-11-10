# -*- coding: utf-8 -*-
# clustering code classes:
# fill hit map with gaussians (pseudo-alphs)

#import ROOT
import numpy as np
import math


#########################
######## Basic parameters
#########################

squareWidth=25 #specied by user
occupancy=4 #specified by user
cluWidth=3
cluToT=3500
cluPeak=200
cluTHL=5
cluSig=2*cluWidth/(2*np.sqrt(2*np.log(cluPeak/cluTHL)))

#rand=ROOT.TRandom1()

#########################
######## Print Functions
#########################

def printBasic():
	print "Basic Parameters..."
	print "squareWidth:", squareWidth
	print "occupancy:", occupancy
	print "cluWidth:", cluWidth
	print "cluToT:", cluToT
	print "cluPeak:", cluPeak
	print "cluTHL:", cluTHL
	print "cluSig:", cluSig

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
        outStr="\x1b["+str(col)+"m"+outStr+"\x1b[0m"
        
    #print outStr
    return outStr


def ShowArray(arr,arrEl=2,opt="off log"):
    
    el=arrEl
    
    doDigi=False
    doCol=False
    doIndex=False
    if el>=len(arr[0]):
        print "specified element (",el,") beyond limit of array element:",len(arr[0]),". Using element 0."
        el=0
    elif el<0:
        print "-ve value --> binary fudge!"
        el=el*-1
        doDigi=True
        
    if "col" in opt or "Col" in opt:
        doCol=True
        
    if "ind" in opt or "Ind" in opt:
        doIndex=True
        
    row=0
    rowStr=""
    count=0
    for a in arr:
        #print "pos:",pos
        if a[1]!=row:
            print rowStr
            row=a[1]
            rowStr=""
            
        val=a[el]
        
        if doDigi==True:
            dig=0
            if(a[el]>cluTHL):
                dig=1
            val=dig
        
        if doIndex==True:
            val=count
        
        if doCol==True:
            rowStr=rowStr+" "+int2Colour(val,a[2], opt)
        else:
            rowStr=rowStr+" "+str(val)
            
        count=count+1
    print rowStr #catch last row

#########################
######## Charge distribution Functions
#########################

def DotProd(a,b,lim=-1):
    total=0
    max=0
    if lim>0:
        max=lim
    else:
        max=len(a)
    
    if len(a)<max or len(b)<max:
        print "DotProd: array mismatch... a:",len(a),", b:",len(b),", max:",max
    else:
        for i in range(0,max,1):
            total=total+a[i]*b[i]
    return total

def CalcDist(a,b,lim=-1):
    diff=[]
    dist=0
    max=0
    if lim>0:
        max=lim
    else:
        max=len(a)

    if len(a)<max or len(b)<max:
        print "CalcData: array mismatch... a:",len(a),", b:",len(b),", max:",max
    else:
        for i in range(0,max,1):
            diff.append(a[i]-b[i])
        dist=math.sqrt(diff[0]*diff[0]+diff[1]*diff[1])
    return dist

def Mag(a,lim=-1):
    mag=0.0
    max=0
    if lim>0:
        max=lim
    else:
        max=len(a)

    if len(a)<max:
        print "Mag: array mismatch... a:",len(a),", max:",max
    else:
        for i in range(0,max,1):
            mag=mag+a[i]*a[i]
            #print "a:",a[i],"...",mag
        mag=math.sqrt(mag)
    return mag



#########################
######## Charge distribution Functions
#########################

def IntegrateGaussianFrac( A, Bx, Cx, By, Cy, xlo=-1.0, xhi=-1.0, ylo=-1.0, yhi=-1.0 ):
    
    val=0.0;
    val = A*2*np.pi*Cx*Cy
    skip=True
    
    if(xlo>=xhi): # full integral in x
        val= val*1
        skip=True
        print "ignore x integral limits" 
    else:
        x0=xlo
        x1=xhi
        zx0 = (x0-Bx)/np.sqrt(2*Cx*Cx);
        zx1 = (x1-Bx)/np.sqrt(2*Cx*Cx);
        val = val * ( math.erf(zx1) + 1 )/2 - ( math.erf(zx0) + 1 )/2 # integral without constants
    
    if(ylo>=yhi): # full integral in y
        val= val *1 
        skip=True
        print "ignore y integral limits" 
    else:
        y0=ylo
        y1=yhi
        zy0 = (y0-By)/np.sqrt(2*Cy*Cy);
        zy1 = (y1-By)/np.sqrt(2*Cy*Cy);
        val = val * ( math.erf(zy1) + 1 )/2 - ( math.erf(zy0) + 1 )/2 #integral without constants

    if skip:
        val = val / (2*np.pi*Cx*Cy)
        
    z=-1.0
    if(ylo<yhi and xlo<xhi):
        z=(-math.erf((x1 - Bx)/(math.sqrt(2.)*Cx)) + math.erf((x0 - Bx)/(math.sqrt(2.)*Cx)));
        z = z * (-math.erf((y1 - By)/(math.sqrt(2.)*Cy)) + math.erf((y0 - By)/(math.sqrt(2.)*Cy)));
        z = z * A * 1/4.0                
    
    #print "Gaus: ",A,", ",Bx,", ",Cx,", ",By,", ",Cy
    #print "\nlimits: ",xlo,"->",xhi,", ",ylo,"->",yhi
    #print "\n val: ",val
    #print "\n alt: ",z
    
    return z

#########################
######## Array Functions
#########################

def Index2Pos(ind):
    global squareWidth
    width=squareWidth
    
    posX=int(ind%width)
    posY=int((ind-posX)/width)
    cont=1
    return [posX,posY,cont]


def UniArr(arr,val=0):
    for a in arr:
        a[2]=val


def ArrLims(arr, subLim=-1):
    xLim=0
    yLim=0
    count=0
    for a in arr:
        if subLim<0 or count<subLim:
            if a[0]>xLim:
                xLim=a[0]
            if a[1]>yLim:
                yLim=a[1]
        count=count+1
    return [xLim,yLim]

def ApplyTHL(arr,thl):
    for a in arr:
        if a[2]<thl:
            a[2]=0

def GetHits(occ, opt=""):
    global squareWidth
    hits=[]
    for i in range(0,occupancy,1):
        #numX=rand.Uniform(0,squareWidth)
        #numY=rand.Uniform(0,squareWidth)
        numX=np.random.uniform(0,squareWidth)
        numY=np.random.uniform(0,squareWidth)
        if "debug" in opt:
            print "i_",i,":",numX,",",numY," ... ToT: ",cluToT
    
        centX= numX-np.floor(numX)
        centY= numY-np.floor(numY)
        #print "i_",i,"\':",centX,",",centY
        combCont=0.0
        checkWidth=cluWidth+2
        for r in range(0-checkWidth,0+checkWidth+1,1):
            for s in range(0-checkWidth,0+checkWidth+1,1):
                #if (r*r+s*s)>checkWidth*checkWidth:
                #continue
                cont = IntegrateGaussianFrac(cluToT,centX,cluSig,centY,cluSig,r,r+1,s,s+1)
                combCont=combCont+cont
                #cont = IntegrateGaussianFrac(10,centX,0.1,centY,0.1,r,0,r,0)
                hits.append([int(numX)+r,int(numY)+s,cont])
                #print "r_",r," s_",s,":",cont
        if "debug" in opt:
            print "i_",i,"\':",centX,",",centY," ... tot': ",combCont
    return hits


def AddHits(arr,hitArr,opt=""):
    
    arrLims=ArrLims(arr)
    for h in hitArr:
        hit=h
        if "index" in opt:
            hit=arr[h]
            hit[2]=1
        #print h
        
        if int(hit[0])>arrLims[0]:
            print "hit out of X scope:",int(hit[0])," >",arrLims[0]
            continue
        if int(hit[1])>arrLims[1]:
            print "hit out of Y scope:",int(hit[1])," >",arrLims[1]
            continue
        for a in arr:
            #print a
            if a[0]==int(hit[0]) and a[1]==int(hit[1]):
                a[2]=a[2]+hit[2]
                #print "hit added:",a[0],",",a[1]," (",hit[0],",",hit[1],")"
                break


def AddColHits(arr,hitArr,col=41, opt=""):
    
    arrLims=ArrLims(arr)
    for h in hitArr:
        hit=h
        if "index" in opt:
            hit=arr[h]
        
        if int(hit[0])>arrLims[0]:
            print "hit out of X scope:",int(hit[0])," >",arrLims[0]
            continue
        if int(hit[1])>arrLims[1]:
            print "hit out of Y scope:",int(hit[1])," >",arrLims[1]
            continue
        for a in arr:
            #print a
            if a[0]==int(hit[0]) and a[1]==int(hit[1]):
                a[2]=col
                #print "hit added:",a[0],",",a[1]," (",hit[0],",",hit[1],")"
                break


#########################
######## Custering Functions
#########################

def checkNeighbours(arr,index, clus):
    global squareWidth
    width=squareWidth
    pos=index
    
    if(arr[index][2]==0.0):
        return pos
    
    if index+1>=len(arr):
        return pos
        
    if(arr[index+1][2]>0.0 and (index+1)%width>(index)%width):
        if(index+1 not in clus):
            clus.append(index+1)
            pos=checkNeighbours(arr,index+1,clus)

    if index-1<0:
        return pos
    
    if(arr[index-1][2]>0.0 and (index-1)%width<(index)%width):
        if(index-1 not in clus):
            clus.append(index-1)
            pos=checkNeighbours(arr,index-1,clus)
            
    if index+width>=len(arr):
        return pos
    
    if(arr[index+width][2]>0.0):
        if(index+width not in clus):
            clus.append(index+width)
            pos=checkNeighbours(arr,index+width,clus)

    if index-width<0:
        return pos
    
    if(arr[index-width][2]>0.0):
        if(index-width not in clus):
            clus.append(index-width)
            pos=checkNeighbours(arr,index-width,clus)
    
    return pos


def ClusterArray(arr):
    global squareWidth
    width=squareWidth
    last=-1
    clusters=[]
    for a in range(0,len(arr),1):
        skip=False
        for c in clusters:
            if(a in c):
                skip=True
                break
        if skip==True:
            continue
        #print "a:",a
        if arr[a][2]>0.0:
            clus=[a]
            checkNeighbours(arr,a,clus)
            #print "clu_",len(clusters),":",len(clus)
            #print clus
            #last=max(clus)
            clusters.append(clus)
            
    reps=0
    for c in range(0,len(clusters),1):
        for d in clusters[c]:
            if c+1>=len(clusters):
                continue
            if d in clusters[c+1]:
                print "shared index:",d
                reps=reps+1
    
    
    for c in range(0,len(clusters),1):
        tot=0
        for d in clusters[c]:
            tot=tot+arr[d][2]
        print "ToT c_",c,":",tot
    
    print "number shared indices:",reps
                
    return clusters


def ClusterParams(cluster, col=-1, opt=""):
    extX=[1e6,-1]
    extY=[1e6,-1]
    signal=0
    size=0
    for h in cluster:
        hit=Index2Pos(h)
        signal=signal+hit[2]
        size=size+1
        if hit[0]<extX[0]:
            extX[0]=hit[0]
        if hit[0]>extX[1]:
            extX[1]=hit[0]
        if hit[1]<extY[0]:
            extY[0]=hit[1]
        if hit[1]>extY[1]:
            extY[1]=hit[1]

    if "silent" not in opt:
        if col<0:
            print "cluster... cluSize: ",size,", cluSizeX:",extX[1]-extX[0]+1,", cluSizeY:",extY[1]-extY[0]+1,", cluSignal:", signal
        else:
            print "\x1b["+str(col)+"m"+"cluster..."+"\x1b[0m"+" cluSize: ",size,", cluSizeX:",extX[1]-extX[0]+1,", cluSizeY:",extY[1]-extY[0]+1,", cluSignal:", signal

    return [size,extX[1]-extX[0]+1,extY[1]-extY[0]+1,signal]


def HitNeighbours(arr,index):
    global squareWidth
    width=squareWidth
    filled=0
    #left-right
    if((index-1)>-1 and arr[index-1][0]<arr[index][0] and arr[index-1][2]>0):
        filled=filled+1
        #print "A"
    if((index+1)<len(arr) and arr[index+1][0]>arr[index][0] and arr[index+1][2]>0):
        filled=filled+1
        #print "B"
    #up-down
    if((index-width)>-1 and arr[index-width][1]<arr[index][1] and arr[index-width][2]>0):
        filled=filled+1
        #print "C"
    if((index+width)<len(arr) and arr[index+width][1]>arr[index][1] and arr[index+width][2]>0):
        filled=filled+1
        #print "D"
    #diagonals (below)
    if((index-1+width)<len(arr) and arr[index-1+width][0]<arr[index][0] and arr[index-1+width][1]>arr[index][1] and arr[index-1+width][2]>0):
        filled=filled+1
        #print "E"
    if((index+1+width)<len(arr) and arr[index+1+width][0]>arr[index][0] and arr[index+1+width][1]>arr[index][1] and arr[index+1+width][2]>0):
        filled=filled+1
        #print "F"
    #diagonals (above)
    if((index-1-width)>-1 and arr[index-1-width][0]<arr[index][0] and arr[index-1-width][1]<arr[index][1] and arr[index-1-width][2]>0):
        filled=filled+1
        #print "G"
    if((index+1-width)>-1 and arr[index+1-width][0]>arr[index][0] and arr[index+1-width][1]<arr[index][1] and arr[index+1-width][2]>0):
        filled=filled+1
        #print "H"
    #print "index:",index," ... ",filled
    return filled


def CalcPerimeter(arr,hitArr):
    count=0
    perArr=[]
    for c in hitArr:
        perimeter=[]
        for h in c:
            cluPer=HitNeighbours(arr,h)
            if cluPer<8:
                perimeter.append(h)
        perArr.append(perimeter)
        print "clu_",count,"(",len(c),"):",len(perimeter)
        count=count+1
    return perArr

def ClusterMean(arr, opt=""):
    mean=[0,0,0]
    for a in arr:
        hit=a
        if "index" in opt:
            hit=Index2Pos(a)
        for i in range(0,len(hit),1):
            mean[i]=mean[i]+hit[i]

    for i in range(0,len(mean),1):
        mean[i]=mean[i]/len(arr)

    return mean


def Circularity(perArr,cluArr):

    cluArea=[]
    for c in cluArr:
        cluArea.append(len(c))
    #print cluArea
    cluPer=[]
    for p in perArr:
        cluPer.append(len(p))
    #print cluPer
    circ = []

    if len(cluPer)!=len(cluArea):
        print "array mismatch... areas:",cluArea,", perimeters:",cluPer
    else:
        for i in range(0,len(cluArea),1):
            circ.append((4*math.pi*cluArea[i])/(cluPer[i]*cluPer[i]))

    return circ

def TransverseAxis(arr, opt=""):
    
    #T⊥= max|n⊥|=1 ∑i|n⊥×pi⊥|/(∑i|pi⊥|)
    
    mean=ClusterMean(arr,opt)
    
    #print "mean:",mean
    maxVec=[]
    maxVal=-1
    
    for p in arr:
        pHit=p
        if "index" in opt:
            pHit=Index2Pos(p)
        nVec=[]
        for i in range(0,len(pHit),1):
            nVec.append(pHit[i]-mean[i])
        sumD=0.0
        sumN=0.0
        #print "pHit:",pHit,", adjusted:",nVec
        for q in arr:
            qHit=q
            if "index" in opt:
                qHit=Index2Pos(q)
            qVec=[]
            for i in range(0,len(qHit),1):
                qVec.append(qHit[i]-mean[i])
            #print "nVec:",nVec,", qVec:",qVec,", dot:",DotProd(nVec,qVec,2),", mag:",Mag(qVec,2)
            sumN=sumN+DotProd(nVec,qVec,2)
            sumD=sumD+Mag(qVec,2)
        sumR=0.0
        if sumD>0:
            sumR=sumN/sumD
        #print "sum[N,D,R]:",[sumN,sumD,sumR]
        if sumR>maxVal:
            maxVal=sumR
            #print "Update maxVal:",sumR,"...",nVec
            maxVec[:]=[]
            for i in range(0,len(nVec),1):
                maxVec.append(nVec[i]+mean[i])
            #print "maxVec:",maxVec
    
    #print "maxVal",maxVal," --> ",maxVec
    return maxVec










