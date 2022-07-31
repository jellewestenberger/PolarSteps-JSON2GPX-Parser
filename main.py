import os 
import datetime
import numpy as np
import glob
import subprocess

# converting json files (polarsteps export)
def convertjson(gpsdat,name):
    dat=open(gpsdat)
    waypoints=dat.readlines()
    dat.close()

    waypoints=waypoints[0].split('[')
    waypoints=waypoints[1].split('{')

    lon=[]
    lat=[]
    timel=[]

    print("Parsing..") 
    for i in range(len(waypoints)):
        if i%100==0:
            print("%f " %((100.*i/len(waypoints))))
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

    lines=['<?xml version="1.0" encoding="UTF-8" ?><gpx version="1.0" creator="%s" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.topografix.com/GPX/1/0" xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd">\n \n <trk><trkseg>\n'%name]

    for i in range(len(timel)):
        date=datetime.datetime.fromtimestamp(timel[i])
    

    
        ds=date.isoformat()+"Z" # Indicates UTC time
        s='<trkpt lat="%f" lon="%f"><time>%s</time><src>polarsteps</src></trkpt>\n' %(lat[i],lon[i],ds)
        lines.append(s)
    lines.append("</trkseg></trk></gpx>")
    exp=open(gpsdat[:-5]+"_converted.gpx", "w+")
    exp.writelines(lines)
    exp.close()
    print("Done,\n exported to %s"%(gpsdat[:-5]+"_converted.gpx"))

# converting csv files (influxdb export)
def convertcsv(file):
    source = "influxdb"
    outputfile = open(file.replace(".csv","_converted.gpx"),'w')

    data =np.genfromtxt(file,delimiter=",",skip_header=1,dtype='str')

    lines = ['<?xml version="1.0" encoding="UTF-8" ?><gpx version="1.0" creator="Jelle Westenberger" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.topografix.com/GPX/1/0" xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd">\n','<trk><trkseg>\n\n']
    for i in range(len(data)):
        line = data[i]

        if line[1]!="":
            time = line[0].replace('"','')

            lat = line[1].replace('"','')
            lon = line[2].replace('"','')
            lines.append('<trkpt lat="%s" lon="%s"><time>%s</time><src>%s</src></trkpt>\n' % (lat,lon,time,source))
    lines.append("</trkseg></trk></gpx>")

    outputfile.writelines(lines)
    outputfile.close()
    print("Done,\n exported to %s"%outputfile.name)


jsonfiles = glob.glob("./*.json")
print("found %i json files:" % (len(jsonfiles)))

try:
    name = subprocess.check_output("git config user.name", shell=True).decode("utf-8").replace('\n','')
    print("using git name: %s" % (name))
except:
    name = str(input("Input your name: "))

for f in jsonfiles:
    print("- %s" % (f))
    convertjson(f,name)

csvfiles = glob.glob("./*.csv")
print("found %i csv files:" % (len(csvfiles)))
for f in csvfiles:
    print("- %s" % (f))
    convertcsv(f)
