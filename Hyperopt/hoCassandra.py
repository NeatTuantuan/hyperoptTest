from hyperopt import hp, fmin, rand, tpe, space_eval
import sys, os, time, re,signal
from subprocess import Popen, PIPE

yaml = "/home/ubuntu/Desktop/cassss/conf/cassandra.yaml"
yamlDefault = "/home/ubuntu/Desktop/cassss/conf/cassandraDefault.yaml"
cmd = "/usr/lib/jvm/ycsb-cassandra-binding-0.10.0/cassandraRun.sh"
start = "/usr/lib/jvm/ycsb-cassandra-binding-0.10.0/start.sh"
logPath = "/home/ubuntu/Desktop/result/hoCassandra.csv"

paramNames = [
    "column_index_size_in_kb",
    "commitlog_segment_size_in_mb",
    "commitlog_sync",
    "commitlog_sync_period_in_ms",
    "compaction_preheat_key_cache",
    "compaction_throughput_mb_per_sec",
    "in_memory_compaction_limit_in_mb",
    "memtable_flush_queue_size",
    "multithreaded_compaction",
    "reduce_cache_capacity_to",
    "reduce_cache_sizes_at"
]

def copyFile(source, target):
    open(target, "w").write(open(source, "r").read())
def appendConfig(target, configs):
    open(target, "a").write(configs)


open(logPath, "w").write(",".join(paramNames) + "," + "Throughput")



space = [
    hp.uniform(paramNames[0], 32, 129),
    hp.choice(paramNames[1], ['8','16','32']),
    hp.choice(paramNames[2], ['periodic','batch']),
    hp.uniform(paramNames[3], 10000, 20001),
    hp.choice(paramNames[4], ['true','false']),
    hp.uniform(paramNames[5], 16, 33),
    hp.uniform(paramNames[6], 32, 129),
    hp.uniform(paramNames[7], 4, 9),
    hp.choice(paramNames[8], ['true', 'flase']),
    hp.uniform(paramNames[9], 0, 11),
    hp.uniform(paramNames[10], 0, 10)
]

def changeConfig(configs):
    configList = []
    for config in configs:
        configList.append(str(config))

    configString = ""

    if(configList[2] == "batch"): 
        configString += ("\n" + paramNames[0] + ":" + str(round(float(configList[0]))))
        configString += ("\n" + paramNames[1] + ": " + configList[1])
        configString += ("\n" + "commitlog_sync_batch_window_in_ms" + ": " + "50")
        configString += ("\n" + paramNames[3] + ": " + str(round(float(configList[3]))))
        configString += ("\n" + paramNames[4] + ": " + configList[4])
        configString += ("\n" + paramNames[5] + ": " + str(round(float(configList[5]))))
        configString += ("\n" + paramNames[6] + ": " + str(round(float(configList[6]))))
        configString += ("\n" + paramNames[7] + ": " + str(round(float(configList[7]))))
        configString += ("\n" + paramNames[8] + ": " + configList[8])
        configString += ("\n" + paramNames[9] + ": " + str(round(float(configList[9]))))
        configString += ("\n" + paramNames[10] + ": " + str(round(float(configList[10]))))
    else:
        configString += ("\n" + paramNames[0] + ": " + str(round(float(configList[0]))))
        configString += ("\n" + paramNames[1] + ": " + configList[1])
        configString += ("\n" + paramNames[2] + ": " + configList[2])
        configString += ("\n" + paramNames[3] + ": " + str(round(float(configList[3]))))
        configString += ("\n" + paramNames[4] + ": " + configList[4])
        configString += ("\n" + paramNames[5] + ": " + str(round(float(configList[5]))))
        configString += ("\n" + paramNames[6] + ": " + str(round(float(configList[6]))))
        configString += ("\n" + paramNames[7] + ": " + str(round(float(configList[7]))))
        configString += ("\n" + paramNames[8] + ": " + configList[8])
        configString += ("\n" + paramNames[9] + ": " + str(round(float(configList[9]))))
        configString += ("\n" + paramNames[10] + ": " + str(round(float(configList[10]))))
    
    copyFile(yamlDefault,yaml)
    appendConfig(yaml, configString)
    open(logPath, "a").write("\n")
    open(logPath, "a").write(",".join(configList))




def q(args):
    g = open('/home/ubuntu/Desktop/cassss/bin/cassandra.pid', 'r')
    pid = int(g.readlines()[0])
    try:
        a = os.kill(pid, signal.SIGKILL)
        print ('killed cassandra process(pid:%d) ,return code is %s' % (pid, a))
    except OSError as e:
        print ('no such process')
    g.close()
    time.sleep(3)

    changeConfig(args)
    
    os.system(start)
    time.sleep(5)
    os.system(cmd)

    f = open('/usr/lib/jvm/ycsb-cassandra-binding-0.10.0/run.dat', 'r')
    try:
        Throughput = float(f.readlines()[1].split(", ")[2][:-1])
    except:
        Throughput = 0

    open(logPath, "a").write(","+str(Throughput))



best = fmin(q, space, algo=rand.suggest, max_evals=10)
print(best)
