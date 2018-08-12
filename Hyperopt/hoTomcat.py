from hyperopt import hp, fmin, rand, tpe, space_eval
import sys, os, time, re
import xml.etree.ElementTree as ET
from subprocess import Popen, PIPE


def copyFile(source, target):
    open(target, "w").write(open(source, "r").read())


def appendConfig(target, configs):
    open(target, "a").write(configs)


def insertFisrtLine(line, target):
    with open(target, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line + content)


shutdownTC = "/root/smac-tomcat/run1.sh"
startTC = "/root/smac-tomcat/run2.sh"

catalina = "/usr/tomcat/bin/catalina.sh"
catalinaDefault = "/root/smac-tomcat/catalinaDefault.sh"
serverXML = "/usr/tomcat/conf/server.xml"
serverXMLDefault = "/root/smac-tomcat/serverDefault.xml"
# logPath = "/root/Desktop/TomcatResult/result.csv"
logPath = "/root/hoResult/result.csv"

paramNames = [
    "-XX:PermSize",
    "-XX:MaxNewSize",
    "-XX:MaxPermSize",
    "-Xms",
    "-Xmx",
    "protocol",
    "maxHttpHeaderSize",
    "maxThreads",
    "minSpareSize",
    "MaxSpareSize",
    "minProcessors",
    "acceptCount",
    "enableLookups",
    "connectionTimeout",
    "disableUploadTimeout",
    "compressionMinSize"
]

if (os.path.exists(logPath) == False):
    open(logPath, "w").write(",".join(paramNames) + "," + "throughput")
open(logPath, "a").write("\n")

# os.system(shutdownTC)

# copyFile(catalinaDefault, catalina)
# copyFile(serverXMLDefault, serverXML)

space = [
    hp.choice(paramNames[0], ['128m', '256m', '64m']),
    hp.choice(paramNames[1], ['256m', '128m', '512m']),
    hp.choice(paramNames[2], ['512m', '256m', '1024m']),
    hp.choice(paramNames[3], ['128m']),
    hp.choice(paramNames[4], ['512m', '256m']),
    hp.choice(paramNames[5], ['org.apache.coyote.http11.Http11Protocol', 'org.apache.coyote.http11.Http11NioProtocol',
                              'org.apache.coyote.http11.Http11AprProtocol']),
    hp.choice(paramNames[6], ['8192', '4096', '16384']),
    hp.choice(paramNames[7], ['1000', '500', '2000']),
    hp.choice(paramNames[8], ['100', '200', '50']),
    hp.choice(paramNames[9], ['75', '250', '500']),
    hp.choice(paramNames[10], ['10', '50', '100']),
    hp.choice(paramNames[11], ['100', '50', '200']),
    hp.choice(paramNames[12], ['True', 'false']),
    hp.choice(paramNames[13], ['30000', '3000', '1000']),
    hp.choice(paramNames[14], ['True', 'false']),
    hp.choice(paramNames[15], ['2048', '1024'])
]


def changeConfig(configs):
    configList = []
    for config in configs:
        configList.append(str(config))

    copyFile(catalinaDefault, catalina)
    copyFile(serverXMLDefault, serverXML)

    configString = 'JAVA_OPTS="'
    configString += (' ' + paramNames[0] + '=' + configList[0])
    configString += (' ' + paramNames[1] + '=' + configList[1])
    configString += (' ' + paramNames[2] + '=' + configList[2])
    configString += (' ' + paramNames[3] + configList[3])
    configString += (' ' + paramNames[4] + configList[4] + '";\n')

    insertFisrtLine(configString, catalina)

    tree = ET.parse(serverXML)
    Connector = tree.getroot().find('Service').find('Connector')
    Connector.set(paramNames[5], configList[5])
    Connector.set(paramNames[6], configList[6])
    Connector.set(paramNames[7], configList[7])
    Connector.set(paramNames[8], configList[8])
    Connector.set(paramNames[9], configList[9])
    Connector.set(paramNames[10], configList[10])
    Connector.set(paramNames[11], configList[11])
    Connector.set(paramNames[12], configList[12])
    Connector.set(paramNames[13], configList[13])
    Connector.set(paramNames[14], configList[14])
    Connector.set(paramNames[15], configList[15])
    tree.write(serverXML)




def q(args):
    os.system(shutdownTC)
    changeConfig(args)
    os.system(startTC)

    f = open('/root/Desktop/TomcatResult/dashboard/content/js/dashboard.js', 'r')

    try:
        Throughput = float(f.readlines()[183].split(": [")[1].split(", ")[10])
    except:
        Throughput = 0
    return -Throughput


best = fmin(q, space, algo=rand.suggest, max_evals=10)
print(best)
