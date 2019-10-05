import os 
import datetime
import numpy as np


path=os.path.abspath(__file__)
path=path.replace("\\","/")
fname=path.split("/")[-1]
path=path.replace(fname,"")
files=os.listdir(path)
j=0
print "Located json files: "
while j<len(files):
    if files[j][-4:].lower()=='json':
        print "%s (%d)" %(files[j],j)
        j+=1
    else:
        del files[j]
selfile=files[int(raw_input("select json file "))]
gpsdat=path+selfile
dat=open(gpsdat)
waypoints=dat.readlines()
dat.close()

waypoints=waypoints[0].split('[')
waypoints=waypoints[1].split('{')

lon=[]
lat=[]
timel=[]

print "Parsing.."
for i in range(len(waypoints)):
    if i%100==0:
        print "%f " %((100.*i/len(waypoints)))
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

sortindex = np.argsort(timel)
timel=[timel[i] for i in sortindex]
lon=[lon[i] for i in sortindex]
lat=[lat[i] for i in sortindex]

lines=['<?xml version="1.0" encoding="UTF-8" ?><gpx version="1.0" creator="Jelle Westenberger" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.topografix.com/GPX/1/0" xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd">\n \n <trk><trkseg>\n'] 

for i in range(len(timel)):
    date=datetime.datetime.fromtimestamp(timel[i])
 

 
    ds=date.isoformat()+"Z"
    s='<trkpt lat="%f" lon="%f"><time>%s</time><src>polarsteps</src></trkpt>\n' %(lat[i],lon[i],ds)
    lines.append(s)
    dummy=2
lines.append("</trkseg></trk></gpx>")
exp=open(path+selfile[:-5]+"_converted.gpx", "w+")
exp.writelines(lines)
exp.close()
print "Done,\n exported to %s"%(selfile[:-5]+"_converted.gpx")
try:
    input('Finished')
except:
    dummy=2
