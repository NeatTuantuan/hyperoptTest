#coding:utf-8
from hyperopt import hp, fmin, rand, tpe, space_eval
import sys, os, time, csv

confPath = "/home/master/app/HiBench-master/bin/workloads/sql/join/hadoop/singleRun.csv"
logPath = "/home/master/app/HiBench-master/bin/workloads/sql/join/hadoop/hoResult.csv"
run = "/home/master/app/SMAC/workspace/run.sh"
resultPath = "/home/master/app/HiBench-master/bin/workloads/sql/join/hadoop/time.csv"

def truncateCSV(target):
    with open(target, "r+") as f:
        f.truncate()
        f.close()
def getTime(target):
    with open(target,'r') as csvfile:
        reader = csv.reader(csvfile)
        results= [row for row in reader]
        return results[1][1]

paramNames = [
    "hive.exec.reducers.bytes.per.reducer",
    "hive.exec.parallel.thread.number",
    "hive.join.cache.size",
    "hive.merge.smallfiles.avgsize",
    "hive.mapjoin.bucket.cache.size",
    "hive.map.aggr.hash.percentmemory",
    "hive.stats.fetch.partition.stats",
    "hive.optimize.index.autoupdate",
    "hive.merge.mapfiles",
    "hive.exec.parallel"
]

space = [
    hp.uniform(paramNames[0], 256, 769),
    hp.uniform(paramNames[1], 8, 25),
    hp.uniform(paramNames[2], 25000, 75001),
    hp.uniform(paramNames[3], 16000000, 48000001),
    hp.uniform(paramNames[4], 100, 301),
    hp.uniform(paramNames[5], 5, 9),
    hp.choice(paramNames[6], ['true', 'false']),
    hp.choice(paramNames[7], ['true', 'false']),
    hp.choice(paramNames[8], ['true', 'false']),
    hp.choice(paramNames[9], ['true', 'false']),
]


# truncateCSV(confPath)


#将参数名写入日志中
if(os.path.exists(logPath) == False):
    open(logPath, "w").write(",".join(paramNames) + "," + "time")
open(logPath, "a").write("\n")

#将参数名写入配置文件的csv中

# if(os.path.exists(confPath) == False):
#     open(confPath, "w").write(",".join(paramNames) )
# open(confPath, "a").write("\n")

#将参数写入配置文件csv中
def changeConfig(configs):
    configList = []
    for config in configs:
        configList.append(str(config))


    truncateCSV(confPath)
    open(confPath, "w").write(",".join(paramNames) )

    configSting = ""
    configSting += (str(round(float(configList[0])))+",")
    configSting += (str(round(float(configList[1])))+",")
    configSting += (str(round(float(configList[2])))+",")
    configSting += (str(round(float(configList[3])))+",")
    configSting += (str(round(float(configList[4])))+",")
    configSting += (str(round(float(configList[5]))/10)+",")
    configSting += (configList[6]+",")
    configSting += (configList[7]+",")
    configSting += (configList[8]+",")
    configSting += (configList[9])

    #配置文件中的参数字符串每次循环覆盖
    open(confPath, "a").write("\n")
    open(confPath, "a").write(configSting)

    open(logPath, "a").write("\n")
    open(logPath, "a").write(",".join(configList))


def q(args):
    changeConfig(args)
    os.system(run)

    try:
        time = float(getTime(resultPath))
    except:
        time = 100000

    open(logPath, "a").write(","+str(time))

    return time
    
best = fmin(q, space, algo=rand.suggest, max_evals=300)
print(best)