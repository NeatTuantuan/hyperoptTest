from hyperopt import fmin, tpe, hp, space_eval, rand, STATUS_OK, STATUS_FAIL
import sys, os, time, re
from subprocess import Popen, PIPE

ratio = 16
maxMem = 20480
maxCore = 4
worker = 5
par = 100

timeLimit = 45600
startTime = time.time()

defaultConfPath = "/home/cloud/exper/spark.conf"
targetConfPath = "/home/cloud/HiBench-master/conf/spark.conf"
cmd = "/home/cloud/HiBench-master/bin/workloads/ml/bayes/spark/run.sh"
logPath = "/home/cloud/exper/result/bayes/hyperopt.csv"

paramNames = [
    "spark.executor.cores",
    "spark.executor.memory",
    "spark.memory.fraction",
    "spark.memory.storageFraction",
    "spark.default.parallelism",
    "spark.shuffle.compress",
    "spark.shuffle.spill.compress",
    "spark.broadcast.compress",
    "spark.rdd.compress",
    "spark.io.compression.codec",
    "spark.reducer.maxSizeInFlight",
    "spark.shuffle.file.buffer",
    "spark.serializer"
]


def copyFile(source, target, configs):
    open(target, "w").write(open(source, "r").read())
    open(target, "a").write(configs)

def toMills(seconds):
    return int(round(seconds * 1000))

open(logPath, "w").write(",".join(paramNames) + "," + "time")


def changeConfig(configs):
    configList = []
    for config in configs:
        configList.append(str(config))

    core = int(configList[0]) + 1
    mem = int(configList[1]) + 4140
    parallelism = int(configList[4]) + 20
    configList[0] = str(core)
    configList[1] = str(mem)
    configList[4] = str(parallelism)
    configList[10] = str(int(configList[10]) + 8)
    configList[11] = str(int(configList[11]) + 8) 
    nMExec = int(maxMem / mem)
    nCExec = int(maxCore / core)
    testMem = str(int((mem - 300) / ratio + 300))
    n = min(nCExec, nMExec) * worker * core
    configString = ""
    configString += ("\n" + paramNames[0] + " " + str(core))
    configString += ("\n" + paramNames[1] + " " + testMem + "m")
    configString += ("\n" + paramNames[2] + " " + str(configList[2]))
    configString += ("\n" + paramNames[3] + " " + str(configList[3]))
    configString += ("\n" + paramNames[4] + " " + str(configList[4]))
    configString += ("\n" + paramNames[5] + " " + configList[5])
    configString += ("\n" + paramNames[6] + " " + configList[6])
    configString += ("\n" + paramNames[7] + " " + configList[7])
    configString += ("\n" + paramNames[8] + " " + configList[8])
    configString += ("\n" + paramNames[9] + " " + configList[9])
    configString += ("\n" + paramNames[10] + " " + str(configList[10]) + "m")
    configString += ("\n" + paramNames[11] + " " + str(configList[11]) + "k")
    configString += ("\n" + paramNames[12] + " " + configList[12])
    configString += ("\n" + "spark.cores.max" + " " + str(n))
    copyFile(defaultConfPath, targetConfPath, configString)
    open(logPath, "a").write("\n")
    open(logPath, "a").write(",".join(configList))

def objective(args):
   
    changeConfig(args)
    start_time = time.time()
    io = Popen(cmd.split(" "), stdout=PIPE, stderr=PIPE, shell=True)
    (stdout_, stderr_) = io.communicate()
    runtime = time.time() - start_time
    open(logPath, "a").write("," + str(toMills(runtime)))
    if(time.time() - startTime >= timeLimit):
        sys.exit(0)
    if(io.returncode == 0):
        return {'loss': runtime, 'status': STATUS_OK}
    else:
        return {'loss': runtime, 'status': STATUS_FAIL}

# define a search space
space = [
    hp.randint(paramNames[0], 4),
    hp.randint(paramNames[1], maxMem - 4140 + 1),
    hp.uniform(paramNames[2], 0.1, 0.9),
    hp.uniform(paramNames[3], 0.1, 0.9),
    hp.randint(paramNames[4], par - 20 + 1),

    hp.choice(paramNames[5], ['true', 'false']),
    hp.choice(paramNames[6], ['true', 'false']),
    hp.choice(paramNames[7], ['true', 'false']),
    hp.choice(paramNames[8], ['true', 'false']),
    hp.choice(paramNames[9], ['lz4', 'lzf', 'snappy']),

    hp.randint(paramNames[10], 89),
    hp.randint(paramNames[11], 59),
    hp.choice(paramNames[12], ['org.apache.spark.serializer.JavaSerializer', 'org.apache.spark.serializer.KryoSerializer'])
   
    
]

# minimize the objective over the space
best = fmin(objective, space, algo=tpe.suggest, max_evals=1000000)

print(best)
# -> {'a': 1, 'c2': 0.01420615366247227}
print(space_eval(space, best))
# -> ('case 2', 0.01420615366247227}
