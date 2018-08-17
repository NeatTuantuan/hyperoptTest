import sys, os, time, re,csv

logPath = "/home/master/app/SMAC/workspace/result/HiveResult.csv"
singleRunConfig = "/home/master/app/HiBench-master/bin/workloads/sql/join/hadoop/singleRun.csv"
resultPath = "/home/master/app/HiBench-master/bin/workloads/sql/join/hadoop/time.csv"
run = "/home/master/app/SMAC/workspace/run.sh"

def truncateCSV(target):
    with open(target, "r+") as f:
        f.truncate()
        f.close()
def getTime(target):
    with open(target,'r') as csvfile:
        reader = csv.reader(csvfile)
        results= [row for row in reader]
        return results[1][1]
params = sys.argv[6:]
configMap = dict((name, value) for name, value in zip(params[::2], params[1::2]))

paramNames=[
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

if(os.path.exists(logPath) == False):
    open(logPath, "w").write(",".join(paramNames) + "," + "time")
open(logPath, "a").write("\n")

for name in paramNames:
    line = ""
    line += (str(configMap.get("-" + name)) + ",")
    open(logPath, "a").write(line)

truncateCSV(singleRunConfig)

open(singleRunConfig, "w").write(",".join(paramNames))
open(singleRunConfig, "a").write("\n")
for name in paramNames:
    if name == "hive.exec.parallel":
        open(singleRunConfig, "a").write(str(configMap.get("-" + name)))
    else:
        open(singleRunConfig, "a").write(str(configMap.get("-" + name)) +",")

os.system(run)


try:
    time = float(getTime(resultPath))
except:
    time = 100000

open(logPath, "a").write(str(time))

print("Result for SMAC: %s, 0, 0, %f, 0" % ('SUCCESS', time))
