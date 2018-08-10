import sys, os

defaultConfPath = "/Users/tuantuan/Downloads/hyperopt.docx"
# targetConfPath = "/Users/tuantuan/Downloads/1og.csv"

paramNames = [
    "spark.executor.cores",
    "spark.executor.memory",
    "spark.memory.fraction",
    "spark.memory.storageFraction",
    "spark.default.parallelism",
    "spark.shuffle.compress",
    "spark.shuffle.spill.compress",
    "spark.broadcast.compress",
    "spark.rdd.compress",
    "spark.io.compression.codec",
    "spark.reducer.maxSizeInFlight",
    "spark.shuffle.file.buffer",
    "spark.serializer"
]

def copyFile(source, target, configs):
    # open(target, "w", "UTF-8").write(open(source, "r", "UTF-8").read())
    open(target, "a").write(configs)
if __name__ == '__main__':
    # copyFile(defaultConfPath, "hhhhhhhhh","sssssssssssssssss")
    open(defaultConfPath, "a").write("ssssssssss")