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
# try:
#    cursor.execute(dropDB)
#    cursor.execute(createDB)
#    db.commit()
# except:
#    db.rollback()
# db.close()

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

space = [
    hp.uniform(paramNames[0], 128, 1024*4),
    hp.uniform(paramNames[1], 128, 1024*2),
    hp.uniform(paramNames[2], 128, 2048),
    hp.uniform(paramNames[3], 8, 128),
    hp.uniform(paramNames[4], 1024, 3*1024),
    hp.uniform(paramNames[5], 2*1024, 16*1024),
    hp.uniform(paramNames[6], 0, 2000),
    hp.uniform(paramNames[7], 2000, 50000),
    hp.uniform(paramNames[8], 8*1024, 128*1024),
    hp.uniform(paramNames[9], 2*1024, 128*1024)
]

if(os.path.exists(logPath) == False):
    open(logPath, "w").write(",".join(paramNames) + "," + "throughput")
open(logPath, "a").write("\n")

def changeConfig(configs):
    configList = []
    for config in configs:
        configList.append(str(conf))

    copyFile(confDefault,conf)

    configString = ""
    configString += ("\n"+paramNames[0]+"="+configList[0].split(","[0]))
    configString += ("\n"+paramNames[1]+"="+configList[1].split(","[0]))
    configString += ("\n"+paramNames[2]+"="+configList[2].split(","[0]))
    configString += ("\n"+paramNames[3]+"="+configList[3].split(","[0]))
    configString += ("\n"+paramNames[4]+"="+configList[4].split(","[0]))
    configString += ("\n"+paramNames[5]+"="+configList[5].split(","[0]))
    configString += ("\n"+paramNames[6]+"="+configList[6].split(","[0]))
    configString += ("\n"+paramNames[7]+"="+configList[7].split(","[0]))
    configString += ("\n"+paramNames[8]+"="+configList[8].split(","[0]))
    configString += ("\n"+paramNames[9]+"="+configList[9].split(","[0]))


    open(logPath, "a").write("\n")
    open(logPath, "a").write(",".join(configList))



def q(args):
    changeConfig(args)

    try:
        cursor.execute(dropDB)
        cursor.execute(createDB)
        db.commit()
    except:
        db.rollback()
        db.close()

    os.system(run)
    f = open(resultPath, 'r')

    try:
        Throughput = 
    except:
        Throughput = 0
    open(logPath, "a").write(','+str(Throughput))

    return -Throughput

best = fmin(q, space, algo = rand.suggest, max_evals = 10)
print(best)


