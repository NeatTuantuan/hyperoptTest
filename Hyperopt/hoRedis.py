from hyperopt import hp, fmin, rand, tpe, space_eval
import sys, os, time, re

workload = "/usr/jiaoben/a.txt"
readConf = "/usr/jiaoben/del.sh"

def copyFile(source, target):
    open(target, "w").write(open(source, "r").read())
def appendConfig(target, configs):
    open(target, "w").write(configs)

paramNames = [
    "repl-backlog-size",
    "hash-max-ziplist-value",
    "hash-max-ziplist-entries",
    "list-max-ziplist-size",
    "active-defrag-ignore-bytes",
    "active-defrag-threshold-lower",
    "hll-sparse-max-bytes ",
    "hz",
    "repl-disable-tcp-nodelay"
]

if(os.path.exists(logPath) == False):
    open(logPath, "w").write(",".join(paramNames) + "," + "throughput")
open(logPath, "a").write("\n")

space = [
    hp.uniform(paramNames[0], 1, 11),
    hp.uniform(paramNames[1], 32, 129),
    hp.uniform(paramNames[2], 256, 1025),
    hp.uniform(paramNames[3], -5, 0),
    hp.uniform(paramNames[4], 100, 301),
    hp.uniform(paramNames[5], 5, 21),
    hp.uniform(paramNames[6], 1, 15001),
    hp.uniform(paramNames[7], 1, 501),
    hp.choice(paramNames[8], ['yes', 'no'])
]

def changeConfig(configs):
    configList = []
    for config in configs:
        configList.append(str(config))
    configString = ""
    configString += (configList[0]+" ")
    configString += (configList[1]+" ")
    configString += (configList[2]+" ")
    configString += (configList[3]+" ")
    configString += (configList[4]+" ")
    configString += (configList[5]+" ")
    configString += (configList[6]+" ")
    configString += (configList[7]+" ")
    configString += (configList[8]+" ")

    appendConfig(workload,configString)
    
def q(args):
    changeConfig(args)
    os.system(readConf)