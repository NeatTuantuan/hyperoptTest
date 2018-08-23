from hyperopt import hp, fmin, rand, tpe, space_eval
import sys, os, time, re, pymysql

def copyFile(source, target):
    open(target, "w").write(open(source, "r").read())
def appendConfig(target, configs):
    open(target, "a").write(configs)

confDefault="/root/SMAC/workspace/myDefault.cnf"
conf="/etc/my.cnf"
logPath = "/root/Hyperopt/hoMysql.csv"
run = "/usr/local/tpcc/action.sh"
resultPath = "/usr/local/tpcc/tpcc_mysql_02.log"

db = pymysql.connect("localhost", "root", "123456", charset='utf8' )
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
    "max_heap_table_size",
    "innodb_autoextend_increment",
    "innodb_buffer_pool_size",
    "innodb_additional_mem_pool_size",
    "innodb_log_buffer_size"
]

space = [
    hp.uniform(paramNames[0], 128, 1024*4),
    hp.uniform(paramNames[1], 128, 1024*2),
    hp.uniform(paramNames[2], 128, 2049),
    hp.uniform(paramNames[3], 8, 129),
    hp.uniform(paramNames[4], 1, 4),
    hp.uniform(paramNames[5], 2, 17),
    hp.uniform(paramNames[6], 0, 2000),
    hp.uniform(paramNames[7], 2000, 50000),
    hp.uniform(paramNames[8], 8, 129),
    hp.uniform(paramNames[9], 2, 129),
    hp.uniform(paramNames[10], 8, 513),
    hp.uniform(paramNames[11], 0, 9),
    hp.uniform(paramNames[12], 1, 21),
    hp.uniform(paramNames[13], 4, 33)
]

if(os.path.exists(logPath) == False):
    open(logPath, "w").write(",".join(paramNames) + "," + "TpmC")
open(logPath, "a").write("\n")

def changeConfig(configs):
    configList = []
    for config in configs:
        configList.append(str(config))

    copyFile(confDefault,conf)

    configString = ""
    configString += ("\n"+paramNames[0]+"="+str(round(float(configList[0])))+"KB")
    configString += ("\n"+paramNames[1]+"="+str(round(float(configList[1])))+"KB")
    configString += ("\n"+paramNames[2]+"="+str(round(float(configList[2]))))
    configString += ("\n"+paramNames[3]+"="+str(round(float(configList[3]))))
    configString += ("\n"+paramNames[4]+"="+str(round(float(configList[4])))+"MB")
    configString += ("\n"+paramNames[5]+"="+str(round(float(configList[5])))+"MB")
    configString += ("\n"+paramNames[6]+"="+str(round(float(configList[6]))))
    configString += ("\n"+paramNames[7]+"="+str(round(float(configList[7]))))
    configString += ("\n"+paramNames[8]+"="+str(round(float(configList[8])))+"MB")
    configString += ("\n"+paramNames[9]+"="+str(round(float(configList[9])))+"MB")
    configString += ("\n"+paramNames[10]+"="+str(round(float(configList[10])))+"MB")
    configString += ("\n"+paramNames[11]+"="+str(round(float(configList[11])))+"MB")
    configString += ("\n"+paramNames[12]+"="+str(round(float(configList[12])))+"MB")
    configString += ("\n"+paramNames[13]+"="+str(round(float(configList[13])))+"MB")

    appendConfig(conf,configString)


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
        TpmC = Throughput = float(f.readlines()[-1].split("                 ")[1].split(' ')[0])
    except:
        TpmC = 0
    open(logPath, "a").write(','+str(TpmC))

    return -TpmC

best = fmin(q, space, algo = rand.suggest, max_evals = 300)
print(best)


