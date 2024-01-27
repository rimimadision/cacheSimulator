from collections import OrderedDict

class TwoLevelCache:
    def __init__(self, firCacheSZ, secCacheSZ):
        self.firCacheSZ = firCacheSZ
        self.secCacheSZ = secCacheSZ
        self.firCache = OrderedDict()
        self.secCache = OrderedDict()

    def refer(self, lba):
       raise NotImplementedError('Do not use base class Cache')

    def printResult(self):
        pass

    def printRedundancy(self):
        count = 0
        
        for key1, value1 in self.firCache.items():
            if key1 in self.secCache:
                count += 1
        
        if len(self.secCache) > 0:
            ratio = count / len(self.secCache)
        else:
            ratio = 0.0

        return ratio
