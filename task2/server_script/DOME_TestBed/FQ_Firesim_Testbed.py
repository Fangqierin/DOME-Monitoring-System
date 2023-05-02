import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
#from pathlib import Path
from shapely.geometry import LineString, Polygon#,Point, MultiLineString,MultiPolygon
from shapely.ops import cascaded_union
from collections import defaultdict
import os
import re
#from shapely.geometry import shape 
import pandas as pd
###################
from bcd_helper import imshow, imshow_scatter,imshow_EFA,DrawTask
from FQ_GenTask import GetEFA
from FQ_Task_GeneratorTestbed import  TaskManager 
from FQ_Drones_Info import Sensor, Drone, ReadSen_PPM,LoadDrones
from FQ_FlightPlanning_Comp import AllCompTestbed
from flask import Flask, jsonify, request

app = Flask(__name__)

####################################### Rxfire
def CreateRectangle(x_dl,y_dl, weight,height):# gag 10 m
    #print(weight, height)
    x_r=x_dl#+weight-2
    y_u=y_dl#+height-2
    print(x_dl,x_r)
    #coords=[(x_dl-1,y_dl-1), (x_r,y_dl-1), (x_r,y_u), (x_dl-1,y_u), (x_dl-1, y_dl-1)]
    x_dl=x_dl+weight
    y_dl=y_dl+height
    coords=[(x_dl,y_dl), (x_r,y_dl), (x_r,y_u), (x_dl,y_u), (x_dl, y_dl-1)]
    poly=Polygon(coords)
    return poly 

def ClearBarrier(data):      
    polygons=[]
    for index, row in data.iterrows():
        poly = row['geometry']
        #print(f"seeeee {poly}")
        polygons.append(poly)
    #print(f"whyyyyy {polygons[0]}")
    u=cascaded_union([polygons[0],polygons[1],polygons[2]])
    u2=cascaded_union([polygons[3],polygons[6]])
    x,y=u2.exterior.coords.xy
    newdata = gpd.GeoDataFrame()
    newdata['geometry'] = None
    newdata.loc[0, 'geometry'] = u2.boundary[0]
    newdata.loc[1, 'geometry'] = polygons[4].boundary
    newdata.loc[2, 'geometry'] = u.boundary
    #da2=gpd.read_file(f"{dir}/{foldername}/input/seelin.shp")
    return newdata
    # da2.plot()
    # plt.show()    
# def WriteInput(foldername, dir,step=1,initime=(0,0),dura=(2,0), dis_res=5, pre_res=5): # The simulation time 100 =1:00) duration<24 hours!
#     fin = open(f"{dir}/{foldername}/input/Burn.input", "w")
#     with open(f"{dir}/Template_burn/input/Burn.input", "r") as ftmp:
#         filedata = ftmp.readlines()
#     checkwind=False
#     FARSITE_START_TIME=''
#     for line in filedata:
#         if re.match(r'FARSITE_START_TIME:*',line):
#             time=line[:-1].split(' ')[-1]
#             checkwind=True
#             if initime[0]<10:
#                 time=f"0{initime[0]}"
#             else:
#                 time=f"{initime[0]}"
#             if initime[1]<10:
#                 time=time+f"0{initime[1]}"
#             else:
#                 time=time+f"{initime[1]}"
#             FARSITE_START_TIME=r'05 04 '+f"{time}"
#             fin.write(f"FARSITE_START_TIME: {FARSITE_START_TIME}\n")
#         elif checkwind  and re.match(r'2013 5 4 '+f"{time}",line):
#             wind=int(line[:-1].split(' ')[-3])
#             winddric=int(line[:-1].split(' ')[-2])
#             fin.write(line)
#         elif re.match(r'FARSITE_END_TIME:*',line):
#             ent=[]
#             ent.append(initime[0]+dura[0])
#             if initime[1]+dura[1]>60:
#                 ent[0]=ent[0]+1
#                 ent.append(initime[1]+dura[1]-60)
#             else:
#                 ent.append(initime[1]+dura[1])
#             if ent[0]<10:
#                 time=f"0{ent[0]}"
#             else:
#                 time=f"{ent[0]}"
#             if ent[1]<10:
#                 time=time+f"0{ent[1]}"
#             else:
#                 time=time+f"{ent[1]}"
#             fin.write(f"FARSITE_END_TIME: 05 04 {time}\n")
#         elif re.match(r'FARSITE_TIMESTEP:*',line):
#             fin.write(f"FARSITE_TIMESTEP: {step}\n")
#         elif re.match(f"FARSITE_DISTANCE_RES: ",line):
#             fin.write(f"FARSITE_DISTANCE_RES: {float(dis_res)}\n")
#         elif re.match(f"FARSITE_PERIMETER_RES: ",line):
#             fin.write(f"FARSITE_PERIMETER_RES: {float(pre_res)}\n")
#         else:
#             fin.write(line)
#     fin.close()
    
def WriteInput(foldername, dir,step=1,initime=(0,0),dura=(2,0), dis_res=5, pre_res=5, wind=5,direction=270,seed=-1,InputDict=[]): # The simulation time 100 =1:00) duration<24 hours!
    fin = open(f"{dir}/{foldername}/input/Burn.input", "w")
    with open(f"{dir}/Template_burn/input/Burn_Random.input", "r") as ftmp:
        filedata = ftmp.readlines()
    checkwind=False
    FARSITE_START_TIME=''
    
    if initime[0]<10:
        intime=f"0{initime[0]}"
    else:
        intime=f"{initime[0]}"
    if initime[1]<10:
        intime=intime+f"0{initime[1]}"
    else:
        intime=intime+f"{initime[1]}"
    
    for line in filedata:
        if re.match(r'FARSITE_START_TIME:*',line):
            time=line[:-1].split(' ')[-1]
            FARSITE_START_TIME=r'05 04 '+f"{intime}"
            fin.write(f"FARSITE_START_TIME: {FARSITE_START_TIME}\n")
        elif re.match(r'05 04*',line):
            fin.write(f"05 04 {intime} 2400\n")
        elif checkwind  and re.match(r'2013 5 4 '+f"{time}",line):
            wind=int(line[:-1].split(' ')[-3])
            winddric=int(line[:-1].split(' ')[-2])
            fin.write(line)
        elif seed!=-1 and re.match(f'SPOTTING_SEED:',line): 
            fin.write(f'SPOTTING_SEED: {seed}\n')
        elif re.match(r'FARSITE_END_TIME:*',line):
            ent=[]
            ent.append(initime[0]+dura[0])
            if initime[1]+dura[1]>60:
                ent[0]=ent[0]+1
                ent.append(initime[1]+dura[1]-60)
            else:
                ent.append(initime[1]+dura[1])
            if ent[0]<10:
                time=f"0{ent[0]}"
            else:
                time=f"{ent[0]}"
            if ent[1]<10:
                time=time+f"0{ent[1]}"
            else:
                time=time+f"{ent[1]}"
            fin.write(f"FARSITE_END_TIME: 05 04 {time}\n")
        elif re.match(r'FARSITE_TIMESTEP:*',line):
            fin.write(f"FARSITE_TIMESTEP: {step}\n")
        elif re.match(f"FARSITE_DISTANCE_RES: ",line):
            fin.write(f"FARSITE_DISTANCE_RES: {float(dis_res)}\n")
        elif re.match(f"FARSITE_PERIMETER_RES: ",line):
            fin.write(f"FARSITE_PERIMETER_RES: {float(pre_res)}\n")
        elif len(InputDict)>0 and re.match(f"2013 5 4",line):
            slot=line.split(' ')[3]
            wd, dir=InputDict[slot]
            #elif re.match(f"2013 5 4 0000 58 26 0.00",line):
            fin.write(f"2013 5 4 {slot} 58 26 0.00 {wd} {dir} 0\n")
        elif len(InputDict)==0 and re.match(f"2013 5 4",line):
            slot=line.split(' ')[3]
            fin.write(f"2013 5 4 {slot} 58 26 0.00 {wind} {direction} 0\n")
        else:
            fin.write(line)
    fin.close()

def PutSite(data, UID, Len, Width,foldername, dir, offset=20):
    if len(UID)==1:
        # Get Boundary: 
        # poly=data.loc[UID[0],'geometry']
        # poly=Polygon(poly)
        site=data.loc[UID[0],'geometry']
        x,y=site.coords.xy
        mx,my,bx,by=(min(x),min(y),max(x),max(y))
        #print(f"length: {max(x)-min(x)} width: {max(y)-min(y)}")
        #offset=20
        boundary=(int(min(x)+offset), int(min(y)+offset), (int(min(x))+offset+Len), int(min(y)+offset+Width))
        mx,my,bx,by=boundary
        #poly=CreateRectangle(mx,my,Len,Width)
        coords=[(mx,my), (bx,my), (bx,by), (mx,by), (mx, my)]
        poly=LineString(coords)
        bound_space=(mx, my,bx,by)
        # if poly.geom_type=='Polygon':
        #     feature=[0]
        # else:[data.loc[i,'geometry'] for i in range(len(data))
        #     feature =[i for i in range(len(poly.geoms))] #
        bargdr = gpd.GeoDataFrame()
        bargdr['geometry'] = None
        bargdr.loc[0, 'geometry']=poly #, crs='EPSG:4326)
        # bargdr.plot()
        # plt.show()
    StartTestBed(foldername, bargdr, dir) # Create some folders for output
    return bound_space


def StartTestBed(foldername, bargdr, dir):
    os.system(f"mkdir {dir}/{foldername}")
    os.system(f"cp -r {dir}/Template_burn/input {dir}/{foldername}")
    bargdr.to_file(f"{dir}/{foldername}/input/TestBed.shp")    #------> This is the objective!!!!!! 
    try:
        os.system(f"rm  -r {dir}/{foldername}/output")
        os.system(f"mkdir {dir}/{foldername}/output")
    except:
        #print(f" did we remove the folder????" )
        os.system(f"mkdir {dir}/{foldername}/output")

def RunFarsite_Test(foldername, dir,time,simdur,step=1,wind=10, direction=270):   
    #write testfile
    tmp=[0,0]
    simdur=simdur+10  #I do not why it always stop earlier! 
    if simdur>=60:
        tmp[0]=simdur//60
        tmp[1]=simdur%60
    else:
        tmp[1]=simdur
    #print(f"Sim time {tmp}")
    WriteInput(foldername,dir,dura=tmp, step=step, wind=wind,direction=direction)
    f = open(f"{dir}/{foldername}/{foldername}_TEST.txt", "w")
    f.write(f"{dir}/{foldername}/input/Burn.lcp ")# write landscape
    f.write(f"{dir}/{foldername}/input/Burn.input ") # write input file
    f.write(f"{dir}/{foldername}/input/{foldername}.shp ")# write ignition fire
    f.write(f"{dir}/{foldername}/input/seelin.shp ")
    #f.write(f"{dir}/{foldername}/input/TestBed.shp ")   # We can change the barrier!!! 
    f.write(f"{dir}/{foldername}/output/{time} 0")   # Output
    f.close()
    #print(f"Command: {dir}/src/TestFARSITE {dir}/{foldername}/{foldername}_TEST.txt")
    try:
        out=os.system(f"{dir}/src/TestFARSITE {dir}/{foldername}/{foldername}_TEST.txt")# >/dev/null 2>&1")
        #print(f"see out", out.read())
        print(f"Generate the fire simulation successfully! Simulation from {time} duration  {simdur} ")
    except:
        print(f"Got error when simulating the fire spread")

def AddFireGrid(foldername, dir, prefix, time, poly):   # Update the ignition file! because we add some fire!!!! 
    collection = list(fiona.open(f"{dir}/{foldername}/output/{prefix}_{time}_Perimeters.shp",'r'))
    df1 = pd.DataFrame(collection)
    def isvalid(geom):
            if len(geom['coordinates'][0])>2:
                return 1
            else:
                return 0
    df1['isvalid'] = df1['geometry'].apply(lambda x: isvalid(x))
    df1 = df1[df1['isvalid'] == 1]
    collection = json.loads(df1.to_json(orient='records'))
    #Convert to geodataframe
    data = gpd.GeoDataFrame.from_features(collection)
    try:
        #print(f"{[data.loc[i, 'geometry'] for i in range(len(data))]}")
        geoms=[data.loc[i, 'geometry'] for i in range(len(data))]+[poly.loc[i, 'geometry'] for i in range(len(poly))]
        data2=shapely.ops.unary_union([geom if geom.is_valid else geom.buffer(0) for geom in geoms]) 
    except:
        print(f"some error")
        #data2=cascaded_union([data.loc[i, 'geometry'] for i in range(len(data))])
        geoms=[data.loc[i, 'geometry'] for i in range(len(data))]
        data2=shapely.ops.unary_union([geom if geom.is_valid else geom.buffer(0) for geom in geoms])
    try:
        features = [i for i in range(len(data2))]
        gdr = gpd.GeoDataFrame({'feature': features, 'geometry': data2}) #, crs='EPSG:4326)
    except:
        gdr = gpd.GeoDataFrame({'feature': [0], 'geometry': data2}) #, crs='EPSG:4326)
    gdr.to_file(f"{dir}/{foldername}/input/{foldername}.shp")    #------> This is the objective!!!!!! 
    # gdr.plot()
    # plt.show()

# def EventUpdateEFA(Grid_fire, prefix, time,simdur,BunsiteBound,dir,fname,Res=1):
#     mx,my,_,_=BunsiteBound
#     poly = gpd.GeoDataFrame()
#     i=0
#     for g in list(Grid_fire.keys()):
#         llx,lly=mx+g[0]*Res-Res,my+g[1]*Res-Res
#         fire=CreateRectangle(llx,lly,Res,Res)
#         #print(fire)
#         poly.loc[i,'geometry']=fire
#         i=i+1
#     # poly.plot()
#     # plt.show()
#     #AddFireGrid(fname, dir, prefix, time, poly)
#     RunFarsite_Test(fname, dir,time,simdur=simdur)
#     EFA,EFAdict,bound = GetEFA(time,simdur,BunsiteBound,dir,fname,Res=Res) 
#     mx,my,bx,by=np.array(BunsiteBound)//Res-np.array(bound)//Res
#     bx=EFA.shape[0]+bx
#     by=EFA.shape[1]+by
#     EFA=EFA[int(mx):int(bx),int(my):int(by)]
#     return EFA

####################################### Tow main functions!!!!! 
def UpdateFireIgnition(foldername, dir,BunsiteBound,Grid_map, Res, time,simdur, TM,wind=10,direction=270):   
    mx,my,_,_=BunsiteBound
    x,y=np.where(Grid_map==1)
    #print(f"seeee ", x,y) 
    row, clm=Grid_map.shape
    #print(Grid_map)
    poly = gpd.GeoDataFrame()
    if len(x)==0:
        #TM=TaskManager(Missions)
        EFA=np.full((row,clm),-1)
        
        tasks=TM.StartWithUK(EFA,init=0)
    else:
        for i in range(len(x)):
            llx,lly=mx+x[i]*Res,my+y[i]*Res
            #print(f"see Res", Res)
            fire=CreateRectangle(llx,lly,Res,Res)
            poly.loc[i,'geometry']=fire
        # poly.plot()
        # plt.show()
        gdr=poly
        gdr.to_file(f"{dir}/{foldername}/input/{foldername}.shp")    # Write fire ignition file!  
        #print(f"is it hre????")
        RunFarsite_Test(foldername, dir,time,simdur=simdur,wind=wind, direction=direction) # Run the simulation 
        EFA,EFAdict,bound = GetEFA(inittime,simdur,BunsiteBound,dir,foldername,Res=Res) # Read the output, get EFA
        if len(EFA)==1:
            #It means something is wrong
            print(f"something is wrong")
            RunFarsite_Test(foldername, dir,time,simdur=60,wind=wind, direction=direction) # Run the simulation 
            EFA,EFAdict,bound = GetEFA(inittime,simdur,BunsiteBound,dir,foldername,Res=Res) # Read the output, get EFA
        mx,my,bx,by=np.array(BunsiteBound)//Res-np.array(bound)//Res
        bx=EFA.shape[0]+bx
        by=EFA.shape[1]+by
        EFA=EFA[int(mx):int(bx),int(my):int(by)]
        #imshow(EFA)
        #plt.xlabel('Why (10 Meters)')
        #plt.show()
        #TM=TaskManager(Missions)
        tasks=TM.DeclareGridEFA(EFA,init=0)
    #tasks=TM.DeclareGridEFA(EFA,init=inittime) # Generate tasks 
    return EFA,tasks

Phase2=False

def DrawWPsequence(waypointSeq):
    fig=plt.figure()
    ax=plt.axes(projection='3d')
    ax.plot3D([i[0] for i in waypointSeq], [i[1] for i in waypointSeq],[i[2] for i in waypointSeq])
    ax.scatter([i[0] for i in waypointSeq], [i[1] for i in waypointSeq],[i[2] for i in waypointSeq])
    conw=[w for w in waypointSeq ]
    plt.show()
    
    
if __name__ == "__main__":
#######################Input############################
    # Mission Configuration
    Missions=defaultdict(dict)  #  Missions: period, priority, 
    Missions['BM']=[ 1, 1]  #Burn Site Resource Monitoring (human and equipment)
    Missions['FI']=[ 0.25, 1]  #Fire Intensity Inspection 
    Missions['FT']=[ 0.5, 1]  # track the fire perimeter and the risky area (arrival within 10 min)
    Missions['FD']=[ 0.5, 1] # Fire detection
    ########################Fire Status
    Size=(3,4)### Fire Setting Grid Size
    Grid_map=np.full((Size[0],Size[1]),0)
    Grid_map[0,0]=0
    Grid_map[0,3]=1
    Grid_map[1,3]=1
    Res=0.5 # Grid size
    Plan=1
    ########## Drone  
    inloc=(0.5,0.5,0)# Drone current location
    speeds=[0.4] # Drone Speed
    Plantime=60*Plan# Planning Time
    Wind=15
    Direction=270#180
    ##### Sensor Information
    sensorfile='Data/sensor_info.csv'
    PPMfile='Data/PPM_fake.csv'
########################################Hard Code Part########################
    Len=Size[0]
    Width=Size[1]
    loiter=[1] # Drone loiter time
    GCloc=(0,0,0)
    ranges=[500]
    sensgrp=[['DJI_Air2S']] # Only one drone
    DroneNum=1
    simdur=Plan+10
    ###################################
    dir='farsite'
    file='CARB_BurnUnits/CARB_BurnUnits.shp'
    data=gpd.read_file(f"{dir}/{file}")
    foldername='FQ_test'
    data=ClearBarrier(data)
    BunsiteBound=PutSite(data, [2], Len*Res,Width*Res, foldername, dir) # Create folders and input files! 
    #print(f"BunsiteBound {BunsiteBound}")
    inittime=0
    #Example 1: 
    ##### Get the fire simulation!!! 
    #EFA, tasks=UpdateFireIgnition(foldername, dir, BunsiteBound,Grid_map, Res, inittime,simdur, TM,wind=Wind,direction=Direction)    
    # print(f"see task {tasks} ")
    # print(EFA)
    # imshow_EFA(EFA)
    # DrawTask(tasks,EFA) 
    # plt.show()
    #print(f"Output: Estimated Fire Arrival time: {EFA}")
    #print(f"Output: Tasks {tasks}")
    ########################################
    #sensgrp=[['ZENMUSE_XT2_t','ZENMUSE_XT2_r'],['DJI_Air2S'],['ZENMUSE_XT2_t','ZENMUSE_XT2_r'],['DJI_Air2S'],['ZENMUSE_XT2_t','ZENMUSE_XT2_r'],['ZENMUSE_XT2_t','ZENMUSE_XT2_r']]
    #sensgrp=[['ZENMUSE_XT2_t','ZENMUSE_XT2_r'],['DJI_Air2S'],['ZENMUSE_XT2_t','ZENMUSE_XT2_r'],['ZENMUSE_XT2_t','ZENMUSE_XT2_r']]
    Drones=LoadDrones(sensorfile,PPMfile,DroneNum, speeds, sensgrp, Res,loiter,ranges)
    ########################## Do decomposition~  1: Normal 2: Inter 3: Area 4: Voronoi
    #wind=5
    #logfile=f"./Results/try_{wind}_{STtime}"
    #log=''
    init=0
    TANum=2;GWP=1;FPnum=5
    DecomposeSize=Res
    seed=0
    #WPSeq=AllCompTestbed(TANum,GWP,FPnum,Drones,init, Plantime,inloc,GCloc, Missions,DecomposeSize,EFA, Res,tasks,log='',seed=seed)
    #DrawWPsequence(WPSeq[0])
    #print(f"Output: Waypoint Sequence length {len(WPSeq[0])} {WPSeq[0]}")
    #@app.route('/')
    @app.route('/process_data', methods=['POST'])

    def hello_world():
        data = request.json
        # Extract the defaultdict object and NumPy array from the JSON data
        #Grid_map = defaultdict(dict, data['Grid_map'])
        Missions = defaultdict(dict, data['Missions'])

        Grid_map = np.array(data['Grid_map'])
        Wind = data['Wind']
        Plan=data['Plan']
        simdur=Plan+10
        Direction=data['Direction']
        #print(data)
        #print(wind)
        TM=TaskManager(Missions,theta=1, plantime=Plan) # Create the task manager! 
        EFA, tasks=UpdateFireIgnition(foldername, dir, BunsiteBound,Grid_map, Res, inittime,simdur, TM,wind=Wind,direction=Direction)    
        #Drones=LoadDrones(sensorfile,PPMfile,DroneNum, speeds, sensgrp, Res,loiter,ranges)
        WPSeq=AllCompTestbed(TANum,GWP,FPnum,Drones,init, Plantime,inloc,GCloc, Missions,DecomposeSize,EFA, Res,tasks,log='',seed=seed)
        # return jsonify({'WPS': WPSeq[0]
        #                 }) 
        tasks = {str(key): value for key, value in tasks.items()} # Convert dictionary keys to strings

        return jsonify({'WPS': WPSeq[0], 'EFA': EFA.tolist(), 'Task': tasks})

        #return jsonify({'WPS': WPSeq[0],'EFA':np.array(EFA).tolist(),'Task':tasks}) 
    
    app.run(host='0.0.0.0', port=5000)
    # #Example 2:
    # Grid_fire={(0,6):10, (2,3):10}
    # Update, nEFA, tasks =UpdateReportFire(Grid_fire,simdur,BunsiteBound,dir,foldername,Res, TM)
    # DrawTask(tasks,EFA) 
    
            #return Update
        #Phase2=True
    #Statetrigger.register_insert_trigger(tryUpate, 'fireMap', 'gridStates')
    #Statetrigger.register_update_trigger(tryUpate, 'fireMap', 'gridStates')
    #Statetrigger.register_op_trigger(tryUpate, 'fireMap', 'gridStates')
    #Statetrigger.tail_oplog()
    #print(f" is it over")
    #print(Statetrigger)
    # while True:
    #     pass
    #Statetriggers.stop_tail()
    #DeclareGrid(TG, EFA,init=1, tasks=tasks,Missions=Missions)
########################################### Old code, for something else. 
