import cache
class DoubleLRU(cache.TwoLevelCache):
    def __init__(self, firCacheSZ, secCacheSZ):
        super().__init__(firCacheSZ, secCacheSZ)

    def refer(self, lba):
        hit = 0
        if lba in self.firCache:
            hit = 1
            self.firCache.pop(lba)
        elif len(self.firCache) >= self.firCacheSZ:
            self.firCache.popitem(last=False)
        self.firCache[lba] = 1

        if hit == 0: # Not hit in first level cache
            if lba in self.secCache:
                hit = 2
            elif len(self.secCache) >= self.secCacheSZ:
                self.secCache.popitem(last=False)
                self.secCache[lba] = 1

        return hit


