import sys, os, time, re
from subprocess import Popen, PIPE

def writeConfig(config,target):
    with open(target, "r+") as f:
        f.truncate()
        f.write(config)
        f.close()

run = "/usr/jiaoben/action.sh"
logPath = "/SMAC/workspace/result/smac.csv"
configTarget="/usr/jiaoben/a.txt"
resultPath="/usr/jiaoben/11.txt"

params = sys.argv[6:]
configMap = dict((name, value) for name, value in zip(params[::2], params[1::2]))
config = ""
paramNames=[
    "repl-backlog-size",
    "hash-max-ziplist-value",
    "hash-max-ziplist-entries",
    "list-max-ziplist-size",
    "active-defrag-ignore-bytes",
    "active-defrag-threshold-lower",
    "hll-sparse-max-bytes",
    "hz",
    "repl-disable-tcp-nodelay"
]

if(os.path.exists(logPath) == False):
    open(logPath, "w").write(",".join(paramNames) + "," + "requestsPerSecond")
open(logPath, "a").write("\n")

for name in paramNames:
    line = ""
    line += (str(configMap.get("-" + name)) + ",")
    open(logPath, "a").write(line)
    if name == "repl-backlog-size" or name == "active-defrag-ignore-bytes":
        config+=str(configMap.get("-" + name))+"mb	"
    elif name == "repl-disable-tcp-nodelay":
        config+=str(configMap.get("-" + name))+"\n"
    else:
        config+=str(configMap.get("-" + name))+"	"


writeConfig(config,configTarget)
os.system(run)
try:
    f = open(resultPath, 'r')
    requestsPerSecond = float(f.readlines()[-3].split(" ")[1])
    f.close()
    g = open(resultPath, 'r')
    requestsPerSecond = float(g.readlines()[-3].split(" ")[2])
    g.close()
except:
    f = 0
    g = "CRASHED"

status = "SUCCESS"
if g != "requests":
    status = "CRASHED"

open(logPath, "a").write(str(requestsPerSecond))

print("Result for SMAC: %s, 0, 0, %f, 0" % ('SUCCESS', -requestsPerSecond))





