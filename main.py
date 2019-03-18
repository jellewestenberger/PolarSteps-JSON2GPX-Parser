import numpy as np
import time  
import os 
import datetime

path=os.path.abspath(__file__)
path=path.replace("\\","/")
fname=path.split("/")[-1]
path=path.replace(fname,"")
gpsdat=path+'locations.json'
dat=open(gpsdat)
waypoints=dat.readlines()
dat.close()

waypoints=waypoints[0].split('[')
waypoints=waypoints[1].split('{')

lon=[]
lat=[]
timel=[]


for i in range(len(waypoints)):
    line=waypoints[i]
    line=line.replace(' ', '')
    line=line.replace('}','')
    line=line.replace(']','')
    if len(line)>0:
        line=line.split(',')
        
        for j in range(len(line)):
            seg=line[j].split(':')
            if seg[0]=='"lon"':
                lon.append(float(seg[1]))
            elif seg[0]=='"lat"':
                lat.append(float(seg[1]))
            elif seg[0]=='"time"':
                timel.append(float(seg[1]))



lines=['<?xml version="1.0" encoding="UTF-8" ?><gpx version="1.0" creator="Jelle Westenberger" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.topografix.com/GPX/1/0" xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd">\n \n <trk><trkseg>\n'] 

for i in range(len(timel)):
    date=datetime.datetime.fromtimestamp(timel[i])
 

    test=datetime.datetime.fromtimestamp(1552311342.3)
    ds=date.isoformat()+"Z"
    s='<trkpt lat="%f" lon="%f"><time>%s</time><src>polarsteps</src></trkpt>\n' %(lat[i],lon[i],ds)
    lines.append(s)
    dummy=2
lines.append("</trkseg></trk></gpx>")
exp=open(path+"export.gpx", "w+")
exp.writelines(lines)
exp.close()
print "Done"