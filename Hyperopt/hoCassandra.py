from hyperopt import hp, fmin, rand, tpe, space_eval
import os

cmd = "/usr/lib/jvm/ycsb-cassandra-binding-0.10.0/run.sh"
workload = "/usr/lib/jvm/ycsb-cassandra-binding-0.10.0/workloads/workload"
workloadDefault = "/usr/lib/jvm/ycsb-cassandra-binding-0.10.0/workloads/workloadDefault"
logPath = "/home/ubuntu/Desktop/hyperopt_result/hyperopt.csv"

paramNames = [
    "recordcount",
    "operationcount",
    "fieldcount",
    "fieldlength",
    "readproportion",
    "requestdistribution",
    "fieldlengthdistribution",
    "insertorder"
]

def copyFile(source, target, configs):
    open(target, "w").write(open(source, "r").read())
    open(target, "a").write(configs)


open(logPath, "w").write(",".join(paramNames) + "," + "time")



space = [
    hp.uniform(paramNames[0], 10000, 50000),
    hp.uniform(paramNames[1], 10000, 50000),
    hp.uniform(paramNames[2], 0, 20),
    hp.uniform(paramNames[3], 100, 1000),
    hp.uniform(paramNames[4], 0, 1),
    hp.choice(paramNames[5], ['uniform', 'zipfian', 'latest']),
    hp.choice(paramNames[6], ['zipfian', 'uniform', 'constant']),
    hp.choice(paramNames[7], ['ordered', 'hashed']),
]

def changeConfig(configs):
    configList = []
    for config in configs:
        configList.append(str(config))
    configString = ""
    configString += ("\n" + paramNames[0] + " " + str(round(configList[0], 0).split(".")[0]))
    configString += ("\n" + paramNames[1] + " " + str(round(configList[1], 0).split(".")[0]))
    configString += ("\n" + paramNames[2] + " " + str(round(configList[2], 0).split(".")[0]))
    configString += ("\n" + paramNames[3] + " " + str(round(configList[3], 0).split(".")[0]))
    configString += ("\n" + paramNames[4] + " " + str(round(configList[4], 1).split(".")[0]))
    configString += ("\n" + paramNames[5] + " " + configList[5])
    configString += ("\n" + paramNames[6] + " " + configList[6])
    configString += ("\n" + paramNames[7] + " " + configList[7])
    copyFile(workloadDefault, workload, configString)
    open(logPath, "a").write("\n")
    open(logPath, "a").write(",".join(configList))




def q(args):
    # recordcount, operationcount, fieldcount, fieldlength, readproportion, requestdistribution, fieldlengthdistribution, insertorder = args
    changeConfig(args)
    os.system(cmd)
    f = open('/usr/lib/jvm/ycsb-cassandra-binding-0.10.0/run.dat', 'r')
    try:
        NNthPercentileLatency = float(f.readlines()[-2].split(", ")[2][:-1])
    except:
        NNthPercentileLatency = 0

    return NNthPercentileLatency



best = fmin(q, space, algo=rand.suggest, max_evals=100)
print(best)
