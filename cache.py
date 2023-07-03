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
