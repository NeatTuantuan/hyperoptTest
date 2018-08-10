import sys, os, time, re
import xml.etree.ElementTree as ET
from subprocess import Popen, PIPE

def copyFile(source, target):
    open(target, "w").write(open(source, "r").read())

def insertFisrtLine(line,target):
    with open(target, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line+content)

shutdownTC = "/root/Desktop/smac-tomcat/run1.sh"
startTC = "/root/Desktop/smac-tomcat/run2.sh"

catalina = "/usr/local/tomcat/bin/catalina.sh"
catalinaDefault = "/root/Desktop/smac-tomcat/catalinaDefault.sh"
serverXML = "/usr/local/tomcat/conf/server.xml"
serverXMLDefault = "/root/Desktop/smac-tomcat/serverDefault.xml"
logPath = "/root/Desktop/TomcatResult/result.csv"

params = sys.argv[6:]
configMap = dict((name, value) for name, value in zip(params[::2], params[1::2]))
catalinaLine = ""

paramNames=[
    "XX:PermSize",
    "XX:MaxNewSize",
    "XX:MaxPermSize",
    "Xms",
    "Xmx",
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
catalinaParams=[
    "XX:PermSize",
    "XX:MaxNewSize",
    "XX:MaxPermSize",
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

if(os.path.exists(logPath) == False):
    open(logPath, "w").write(",".join(paramNames)+"," + "throughput")
open(logPath, "a").write("\n")

os.system(shutdownTC)

copyFile(catalinaDefault,catalina)
copyFile(serverXMLDefault,serverXML)

for name in catalinaParams:
    line = ""
    line += (str(configMap.get("--" + name)) + ",")
    open(logPath, "a").write(line)
for name in serverParams:
    line = ""
    line += (str(configMap.get("-" + name)) + ",")
    open(logPath, "a").write(line)

catalinaLine='JAVA_OPTS="-XX:PermSize='+configMap.get("--XX:PermSize")+'m '+'-XX:MaxNewSize='+configMap.get("--XX:MaxNewSize")+'m '+'-XX:MaxPermSize='+configMap.get("--XX:MaxNewSize")+'m '+'-Xms'+configMap.get("--Xms")+'m '+'-Xmx'+configMap.get("--Xmx")+'m"\n'
insertFisrtLine(catalinaLine,catalina)

tree = ET.parse(serverXML)
Connector = tree.getroot().find('Service').find('Connector')
for (key, value) in configMap.items():
    key = key[1:]
    if key in serverParams:
        Connector.set(key,value)
tree.write(serverXML)

os.system(startTC)

f = open('/root/Desktop/TomcatResult/dashboard/content/js/dashboard.js', 'r')
try:
    Throughput = float(f.readlines()[183].split(": [")[1].split(", ")[10])
except:
    Throughput = 0

open(logPath, "a").write(str(Throughput))

print("Result for SMAC: %s, 0, 0, %f, 0" % ('SUCCESS', -Throughput))







