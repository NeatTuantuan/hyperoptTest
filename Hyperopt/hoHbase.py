from hyperopt import hp, fmin, rand, tpe, space_eval
import sys, os, time, re
import xml.etree.ElementTree as ET

configXML = "/home/study/hbase/conf/hbase-site.xml"
confDefault = "/root/Hyperopt/confDefault.xml"
logPath = "/root/Hyperopt/hoHbase.csv"
resultPath = "/root/Hyperopt/result.txt"
run = "/root/Hyperopt/run.sh"

alloConfig = "/root/Hyperopt/ao]lloConfig.sh"
restart = "/root/Hyperopt/restart.sh"
runYcsb = "/root/Hyperopt/runycsb.sh"
exit = "/root/Hyperopt/exit.sh"

paramNames = [
    "hfile.block.cache.size",
    "hbase.regionserver.global.memstore.upperLimit",
    "hbase.regionserver.global.memstore.lowerLimit",
    "hbase.regionserver.handler.count",
    "hbase.hregion.memstore.block.multiplier",
    "hbase.hstore.compactionThreshold",
    "hbase.hstore.blockingStoreFiles",
    "hbase.hregion.memstore.flush.size",
    "hfile.block.index.cacheonwrite",
    "hbase.hregion.memstore.mslab.enabled"
]
space = [
    # hp.choice(paramNames[0], ['0.25', '0.35', '0.45', '0.5']),
    # hp.choice(paramNames[1], ['0.2', '0.3', '0.4', '0.5']),
    # hp.choice(paramNames[2], ['0.15', '0.25', '0.35', '0.45']),
    hp.choice(paramNames[0], ['0.25']),
    hp.choice(paramNames[1], ['0.5']),
    hp.choice(paramNames[2], ['0.15', '0.25', '0.35', '0.45']),
    hp.choice(paramNames[3], ['10', '60', '100', '130', '160', '180', '200']),
    hp.choice(paramNames[4], ['2', '4', '6', '8', '10']),
    hp.uniform(paramNames[5], 3, 11),
    hp.uniform(paramNames[6], 1, 101),
    hp.choice(paramNames[7], ['67108864', '134217728', '1342177280']),
    hp.choice(paramNames[8], ['true', 'false']),
    hp.choice(paramNames[9], ['true', 'false'])
]

if (os.path.exists(logPath) == False):
    open(logPath, "w").write(",".join(paramNames) + "," + "Runtime")

def copyFile(source, target):
    open(target, "w").write(open(source, "r").read())

def changeConfig(configs):
    configList = []
    for config in configs:
        configList.append(str(config))

    # copyFile(confDefault,configXML)

    tree = ET.parse(configXML)
    root = tree.getroot()
    for num in root.iter('property'):
        if(num[0].text == paramNames[0]):
            num[1].text = configList[0]
        elif(num[0].text == paramNames[1]):
            num[1].text = configList[1]
        elif(num[0].text == paramNames[2]):
            num[1].text = configList[2]
        elif(num[0].text == paramNames[3]):
            num[1].text = configList[3]
        elif(num[0].text == paramNames[4]):
            num[1].text = configList[4]
        elif(num[0].text == paramNames[5]):
            num[1].text = str(round(float(configList[5])))
        elif(num[0].text == paramNames[6]):
            num[1].text = str(round(float(configList[6])))
        elif(num[0].text == paramNames[7]):
            num[1].text = configList[7]
        elif(num[0].text == paramNames[8]):
            num[1].text = configList[8]
        elif(num[0].text == paramNames[9]):
            num[1].text = configList[9]

    tree.write(configXML)
    open(logPath, "a").write("\n")
    open(logPath, "a").write(",".join(configList))

def q(args):
    changeConfig(args)
    os.system(run)
    f = open(resultPath, 'r')
    try:
        RunTime = Throughput = float(f.readlines()[1].split(", ")[2][:-1])
    except:
        RunTime = 0
    open(logPath, "a").write(","+str(RunTime))

    return RunTime

best = fmin(q, space, algo=rand.suggest, max_evals=10)
print(best)
