from hyperopt import hp, fmin, rand, tpe, space_eval
import sys, os, time, re
from subprocess import Popen, PIPE

workload = "/usr/jiaoben/a.txt"
resultPath = "/usr/jiaoben/11.txt"
readConf = "/usr/jiaoben/del.sh"
logPath = "/Hyperopt/hoRedis.csv"
run = "/usr/jiaoben/action.sh"

def copyFile(source, target):
    open(target, "w").write(open(source, "r").read())
def writeConfig(config,target):
    with open(target, "r+") as f:
        f.truncate()
        f.write(config)
        f.close()

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
    open(logPath, "w").write(",".join(paramNames) + "," + "requestPerSecond")
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
    configString += (configList[0]+"mb ")
    configString += (configList[1]+" ")
    configString += (configList[2]+" ")
    configString += (configList[3]+" ")
    configString += (configList[4]+"mb ")
    configString += (configList[5]+" ")
    configString += (configList[6]+" ")
    configString += (configList[7]+" ")
    configString += (configList[8]+" \n")

    writeConfig(workload,configString)
    
def q(args):
    changeConfig(args)
    os.system(run)
    try:
        f = open(resultPath, 'r')
        requestsPerSecond = float(f.readlines()[-3].split(" ")[1])
        f.close()
        g = open(resultPath, 'r')
        requestsPerSecond = float(g.readlines()[-3].split(" ")[2])
        g.close()
    except:
        f = 0
        g = "CRASHED"

    status = "SUCCESS"
    if g != "requests":
        status = "CRASHED"

    open(logPath, "a").write(','+str(requestsPerSecond))

    return requestsPerSecond

best = fmin(q, space, algo = rand.suggest, max_evals = 10)
print(best)
