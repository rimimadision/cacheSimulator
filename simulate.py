import argparse
import doubleLRU
import demotion

def object_start_offset(object_id):
    return object_id * (500 * 1024 * 1024)

class CacheSimulator:
    def __init__(self, cache):
        self.cache = cache
        self.numRequets = 0
        self.reqHitInFirstLevel = 0
        self.reqHitInSecondLevel = 0

    def process(self, lba):
        self.numRequets += 1
        hitLevel = self.cache.refer(lba)
        if hitLevel == 0: # Miss in two level
            pass
        elif hitLevel == 1: # Hit in first level
            self.reqHitInFirstLevel += 1
        elif hitLevel == 2: # Hit in second level
            self.reqHitInSecondLevel += 1
        else:
            raise RuntimeError('Undefined Return Value')


    def printSimulateResult(self):
        print(f"Request Num: {self.numRequets}")
        print(f"Host Cache hit: {self.reqHitInFirstLevel}")
        print(f"Device Cache hit: {self.reqHitInSecondLevel}")
        print(f"Host Cache hit ratio: {self.reqHitInFirstLevel/self.numRequets:.8f}")
        print(f"Device Cache hit ratio: {self.reqHitInSecondLevel/(self.numRequets-self.reqHitInFirstLevel):.8f}")
        print(f"Host Cache hit / Request Num: {self.reqHitInFirstLevel/self.numRequets:.8f}")
        print(f"Device Cache hit / Request Num: {self.reqHitInSecondLevel/(self.numRequets):.8f}")
        self.cache.printResult()

def createCache(algo, firCacheSz, secCacheSZ, bs):
    if algo == 'lru':
        return doubleLRU.DoubleLRU(int(firCacheSz / bs),
                                   int(secCacheSZ / bs))
    elif algo == "demotion":
        return demotion.Demotion()
    elif algo == '2Q':
        pass
        #return twoq.TwoQ()
    elif algo == 'slru':
        pass
        #return slru.SLRU()
    else:
        raise RuntimeError('Algorithm not found')

parser = argparse.ArgumentParser(description='命令行参数解析')

# 添加命令行参数
parser.add_argument('-bs', '--block_size', type=int, help='Block Size in KB')
parser.add_argument('-algo', '--algorithm', type=str, help='Algorithm')
parser.add_argument('-trace_file', type=str, help='Trace File Path')
parser.add_argument('-fcsz', '--first_cache_size',
                    type=int, help='First Level Cache Size in MB')
parser.add_argument('-scsz', '--second_cache_size',
                    type=int, help='Second Level Cache Size in MB')

# 解析命令行参数
args = parser.parse_args()
block_size = args.block_size * 1024
first_cache_size = args.first_cache_size * 1024 * 1024
second_cache_size = args.second_cache_size * 1024 * 1024
simulator = CacheSimulator(createCache(args.algorithm,
                                       first_cache_size,
                                       second_cache_size,
                                       block_size))
file_path = args.trace_file

num_lines = 0

with open(file_path, 'r') as file:
    for line in file:
        num_lines += 1
        object_id, start_time, latency, offset, length = line.strip().split(',')
        offset_bytes = int(offset) + object_start_offset(int(object_id))
        length_bytes = int(length)

        start_alignment_offset = int(offset_bytes / block_size)
        end_alignment_offset = int((offset_bytes + length_bytes) / block_size)

        num_blocks = end_alignment_offset - start_alignment_offset + 1

        for i in range(num_blocks):
            simulator.process(start_alignment_offset + i)

simulator.printSimulateResult()
