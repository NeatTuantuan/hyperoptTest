import sys, os, time, re,signal
from subprocess import Popen, PIPE
#from cassandra.cluster import Cluster

def copyFile(source, target):
    open(target, "w").write(open(source, "r").read())
def appendConfig(target, configs):
    open(target, "a").write(configs)

yaml = "/home/ubuntu/Desktop/cassss/conf/cassandra.yaml"
yamlDefault = "/home/ubuntu/Desktop/cassss/conf/cassandraDefault.yaml"
cmd = "/usr/lib/jvm/ycsb-cassandra-binding-0.10.0/cassandraRun.sh"
start = "/usr/lib/jvm/ycsb-cassandra-binding-0.10.0/start.sh"
logPath = "/home/ubuntu/Desktop/result/smac.csv"

configs = ""
g = open('/home/ubuntu/Desktop/cassss/bin/cassandra.pid', 'r')
pid = int(g.readlines()[0])
try:
    a = os.kill(pid, signal.SIGKILL)
    print ('killed cassandra process(pid:%d) ,return code is %s' % (pid, a))
except OSError as e:
    print ('no such process')
g.close()
time.sleep(3)

params = sys.argv[6:]
configMap = dict((name, value) for name, value in zip(params[::2], params[1::2]))

paramNames=[
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

if(os.path.exists(logPath) == False):
    open(logPath, "w").write(",".join(paramNames) + "," + "Throughput")
open(logPath, "a").write("\n")

for name in paramNames:
    line = ""
    line += (str(configMap.get("-" + name)) + ",")
    open(logPath, "a").write(line)    


for (key, value) in configMap.items():
    key = key[1:]
    if key == "commitlog_sync_period_in_ms":
        if configMap['-commitlog_sync'] == "batch":
            configs += "#" + key + ": " + value + "\n"
            configs += "commitlog_sync_batch_window_in_ms: 50\n"
        else:
            configs += key + ": " + value + "\n"
    else:
        configs += key + ": " + value + "\n"

copyFile(yamlDefault,yaml)
appendConfig(yaml, configs)

os.system(start)
time.sleep(5)
os.system(cmd)


f = open('/usr/lib/jvm/ycsb-cassandra-binding-0.10.0/run.dat', 'r')
try:
    Throughput = float(f.readlines()[1].split(", ")[2][:-1])
except:
    Throughput = 0

open(logPath, "a").write(str(Throughput))

print("Result for SMAC: %s, 0, 0, %f, 0" % ('SUCCESS', Throughput))





