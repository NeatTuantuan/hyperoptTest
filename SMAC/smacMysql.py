import sys, os, time, re, pymysql

def copyFile(source, target):
    open(target, "w").write(open(source, "r").read())
def appendConfig(target, configs):
    open(target, "a").write(configs)


confDefault="/root/SMAC/workspace/myDefault.cnf"
conf="/etc/my.cnf"
logPath = "/root/SMAC/workspace/result/MysqlResult.csv"
run = "/usr/local/tpcc/action.sh"
resultPath = "/usr/local/tpcc/tpcc_mysql_02.log"

db = pymysql.connect("localhost", "root", "123456", charset='utf8' )
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
    "max_heap_table_size",
    "innodb_autoextend_increment",
    "innodb_buffer_pool_size",
    "innodb_additional_mem_pool_size",
    "innodb_log_buffer_size"
]

if(os.path.exists(logPath) == False):
    open(logPath, "w").write(",".join(paramNames) + "," + "TpmC")
open(logPath, "a").write("\n")

copyFile(confDefault,conf)
for name in paramNames:
    line = ""
    line += (str(configMap.get("-" + name)) + ",")
    open(logPath, "a").write(line)

config=""
for (key, value) in configMap.items():
    key = key[1:]
    config+=key+"="+value
    if key=="sort_buffer_size" or key=="join_buffer_size":
        config+="KB\n"
    elif key=="thread_cache_size" or key=="max_connect_errors" or key == "max_connections" or key == "table_open_cache":
        config+="\n"
    else:
        config+="MB\n"

appendConfig(conf,config)

os.system(run)

f = open(resultPath, 'r')
try:
    TpmC = Throughput = float(f.readlines()[-1].split("                 ")[1].split(' ')[0])
except:
    TpmC = 0

open(logPath, "a").write(str(TpmC))

print("Result for SMAC: %s, 0, 0, %f, 0" % ('SUCCESS', -TpmC))
