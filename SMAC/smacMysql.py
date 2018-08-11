from hyperopt import hp, fmin, rand, tpe, space_eval
import sys, os, time, re, MySQLdb

def copyFile(source, target):
    open(target, "w").write(open(source, "r").read())
def appendConfig(target, configs):
    open(target, "a").write(configs)


confDefault=""
conf=""
logPath = ""
run=""
resultPath=""

db = MySQLdb.connect("localhost", "root", "123456", charset='utf8' )
cursor = db.cursor()
dropDB = "DROP DATABASE IF EXISTS tpcc100;"
createDB = "CREATE DATABASE tpcc100;"
try:
   cursor.execute(dropDB)
   cursor.execute(createDB)
   db.commit()
except:
   db.rollback()
db.close()

params = sys.argv[6:]
configMap = dict((name, value) for name, value in zip(params[::2], params[1::2]))

paramNames=[
    "sort_buffer_size",
    "join_buffer_size",
    "table_open_cache",
    "thread_cache_size",
    "query_cache_limit",
    "max_allowed_packet",
    "max_connect_errors",
    "max_connections",
    "tmp_table_size",
    "max_heap_table_size"
]

if(os.path.exists(logPath) == False):
    open(logPath, "w").write(",".join(paramNames) + "," + "throughput")
open(logPath, "a").write("\n")

copyFile(confDefault,conf)

for name in paramNames:
    line = ""
    line += (str(configMap.get("-" + name)) + ",")
    open(logPath, "a").write(line)

config=""
for (key, value) in configMap.items():
    key = key[1:]
    config+=key+"="+value+"\n"
appendConfig(conf,config)

os.system(run)

f = open(resultPath, 'r')
try:
    Throughput = 
except:
    Throughput = 0

open(logPath, "a").write(str(Throughput))

print("Result for SMAC: %s, 0, 0, %f, 0" % ('SUCCESS', Throughput))


