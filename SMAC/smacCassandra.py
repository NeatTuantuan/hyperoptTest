import sys, os, time, re
from subprocess import Popen, PIPE
#from cassandra.cluster import Cluster

def copyFile(source, target):
    open(target, "w").write(open(source, "r").read())
def appendConfig(target, configs):
    open(target, "a").write(configs)

cmd = "/usr/lib/jvm/ycsb-cassandra-binding-0.10.0/run.sh"
workload = "/usr/lib/jvm/ycsb-cassandra-binding-0.10.0/workloads/workload"
workloadDefault = "/usr/lib/jvm/ycsb-cassandra-binding-0.10.0/workloads/workloadDefault"
logPath = "/home/ubuntu/Desktop/result/smac.csv"

#cluster = Cluster()
#session = cluster.connect(wait_for_all_pools=True)
#session.execute('truncate usertable.data')
#cluster.shutdown()

params = sys.argv[6:]
configMap = dict((name, value) for name, value in zip(params[::2], params[1::2]))
configs = ""
paramNames=[
    "recordcount",
    "operationcount",
    "readproportion",
    "requestdistribution",
    "fieldcount",
    "fieldlength",
    "insertorder",
    "fieldlengthdistribution"
]

if(os.path.exists(logPath) == False):
    open(logPath, "w").write(",".join(paramNames) + "," + "NNthPercentileLatency")
open(logPath, "a").write("\n")

for name in paramNames:
    line = ""
    line += (str(configMap.get("-" + name)) + ",")
    open(logPath, "a").write(line)    

for (key, value) in configMap.items():
    key = key[1:]
    configs += "\n"
    configs += key
    configs += "="
    if(key == "readproportion"):
        configs += str(int(value)/100)
        configs += "\n"
        configs += "updateproportion"
        configs += "="
        configs += str((100-int(value))/100)
    else:
        configs += value

copyFile(workloadDefault,workload)
appendConfig(workload, configs)

os.system(cmd)


f = open('/usr/lib/jvm/ycsb-cassandra-binding-0.10.0/run.dat', 'r')
try:
    NNthPercentileLatency = float(f.readlines()[-2].split(", ")[2][:-1])
except:
    NNthPercentileLatency = 0

open(logPath, "a").write(str(NNthPercentileLatency))

print("Result for SMAC: %s, 0, 0, %f, 0" % ('SUCCESS', NNthPercentileLatency))





