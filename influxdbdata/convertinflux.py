import os 
import glob
import numpy as np 




def convert(file):
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
            dummy=2
    lines.append("</trkseg></trk></gpx>")

    outputfile.writelines(lines)
    outputfile.close()
    
filelist = glob.glob("./*.csv")

print("\nfiles:\n")
k=0
for f in filelist:
    print("- "+f+" (%i)" % (k))
    convert(filelist[k])
    k+=1

# select = int(input("select file: "))
# file = filelist[select]