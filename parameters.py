# clustering code:
# fill hit map with gaussians (pseudo-alphas)


import ROOT
import numpy as np
import clusteringClass as cc

#######################
########## Executive
#######################

rootFile=ROOT.TFile("params.root","RECREATE","params.root")

cluSize=ROOT.TH1D("cluSize","total cluster",100,0,100)
cluSizeX=ROOT.TH1D("cluSizeX","cluster size in X dimension",20,0,20)
cluSizeY=ROOT.TH1D("cluSizeY","cluster size in Y dimension",20,0,20)
cluSignal=ROOT.TH1D("cluSignal","cluster signal",100,0,100)
cluMult=ROOT.TH1D("cluMult","cluster multiplicity per event",20,0,20)

Nevents=100
cc.occupancy= 5
cc.squareWidth = 40
for e in range(0,Nevents,1):

    sensorArray=[]

    for i in range(0,cc.squareWidth,1):
        for j in range(0,cc.squareWidth,1):
            sensorArray.append([j,i,0]) #x,y,c
    #cc.ShowArray(sensorArray,0,"")
    #cc.printBasic()

    hits=cc.GetHits(cc.occupancy)
    cc.AddHits(sensorArray,hits)
    #cc.ShowArray(sensorArray,2,"col log")
    #cc.printBasic()
    #raw_input("Hits in array. Press return to proceed...")

    cc.ApplyTHL(sensorArray,cc.cluTHL)
    cluArr=cc.ClusterArray(sensorArray)
    #pers=cc.CalcPerimeter(sensorArray,cluArr)

    count=0
    for c in cluArr:
        #print c
        count=count+1
        params=cc.ClusterParams(c,count+40,"silent")
        cluSize.Fill(params[0])
        cluSizeX.Fill(params[1])
        cluSizeY.Fill(params[2])
        cluSignal.Fill(params[3])
    cluMult.Fill(len(cluArr))

rootFile.cd()
cluSize.Write()
cluSizeX.Write()
cluSizeY.Write()
cluSignal.Write()
cluMult.Write()

rootFile.Close()
#cc.printBasic()
#raw_input("Press return to exit")

exit()

