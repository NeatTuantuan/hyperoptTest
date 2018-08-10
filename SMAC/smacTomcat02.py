import sys, os, time, re
import xml.etree.ElementTree as ET
from subprocess import Popen, PIPE

def copyFile(source, target):
    open(target, "w").write(open(source, "r").read())
def appendConfig(target, configs):
    open(target, "a").write(configs)
def insertFisrtLine(line,target):
    with open(target, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line+content)

shutdownTC = "/root/smac-tomcat/run1.sh"
startTC = "/root/smac-tomcat/run2.sh"
catalina = "/usr/tomcat/bin/catalina.sh"
catalinaDefault = "/root/smac-tomcat/catalinaDefault.sh"
serverXML = "/usr/tomcat/conf/server.xml"
serverXMLDefault = "/root/smac-tomcat/serverDefault.xml"
logPath = "/root/TomcatResult/result.csv"

params = sys.argv[6:]
configMap = dict((name, value) for name, value in zip(params[::2], params[1::2]))
catalinaLine = ""

configDic={}

catalinaParams=[
    "XX:MaxNewSize",
    "Xms",
    "Xmx"
]
serverParams=[
    "protocol",
    "maxHttpHeaderSize",
    "maxThreads",
    "minSpareThreads",
    "maxSpareThreads",
    "minProcessors",
    "acceptCount",
    "enableLookups",
    "connectionTimeout",
    "disableUploadTimeout",
    "compressionMinSize"
]

if int(configMap.get("--Xms"))>int(configMap.get("--Xmx")):
    Xms=configMap.get("--Xmx")
    Xmx=configMap.get("--Xms")
else:
    Xmx=configMap.get("--Xmx")
    Xms=configMap.get("--Xms")

MNS=configMap.get("--XX:MaxNewSize")
if int(Xmx)==int(MNS):
    MNS=str(int(Xmx)/2).split('.')[0]
elif int(Xmx)<int(MNS):
    MNS='64'

for (key, value) in configMap.items():
    key=key[1:]
    if key not in serverParams:
        key=key[1:]
        if key=='Xms':
            value=Xms
        elif key=='Xmx':
            value=Xmx
        elif key=='XX:MaxNewSize':
            value=MNS
    configDic[key]=value


if(os.path.exists(logPath) == False):
    open(logPath, "w").write(",".join(catalinaParams+serverParams)+ "," + "errorPersentage" + "," + "time")
open(logPath, "a").write("\n")

os.system(shutdownTC)

copyFile(catalinaDefault,catalina)
copyFile(serverXMLDefault,serverXML)

for name in catalinaParams:
    line = ""
    line += (str(configDic.get(name)) + ",")
    open(logPath, "a").write(line)
for name in serverParams:
    line = ""
    line += (str(configDic.get(name)) + ",")
    open(logPath, "a").write(line)

catalinaLine='JAVA_OPTS="-XX:MaxNewSize='+MNS+'m '+'-Xms'+Xms+'m '+'-Xmx'+Xmx+'m"\n'
insertFisrtLine(catalinaLine,catalina)

tree = ET.parse(serverXML)
Connector = tree.getroot().find('Service').find('Connector')
for (key, value) in configDic.items():
    if key in serverParams:
        Connector.set(key,value)
tree.write(serverXML)

os.system(startTC)



try:
    f = open('/root/TomcatResult/dashboard/content/js/dashboard.js', 'r')
    time = float(f.readlines()[183].split(": [")[1].split(", ")[7])
    f.close()
    g = open('/root/TomcatResult/dashboard/content/js/dashboard.js', 'r')
    ErrorPercentage = float(g.readlines()[183].split(": [")[1].split(", ")[3])
    g.close()  
except:
    time = 0
    ErrorPercentage = 100

open(logPath, "a").write(str(ErrorPercentage)+','+str(time))

if ErrorPercentage > 30:
    status = 'CRASHED'
else:
    status = 'SUCCESS'

print("Result for SMAC: %s, 0, 0, %f, 0" % (status, time))
