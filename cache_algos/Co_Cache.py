import cache
class CoCache(cache.TwoLevelCache):
    def __init__(self, firCacheSZ, secCacheSZ):
        super().__init__(firCacheSZ, secCacheSZ)

    def refer(self, lba):
        hit = 0
        if lba in self.firCache:
            hit = 1
            self.firCache.pop(lba)
            self.firCache[lba] = 1

        if hit == 0: # Not hit in first level cache
            if lba in self.secCache:
                hit = 2
                self.secCache.pop(lba)
                if len(self.firCache) >= self.firCacheSZ:
                    evict_item = self.firCache.popitem(last=False)
                self.firCache[lba] = 1
                self.secCache[evict_item[0]] = 1

        if hit == 0: # Not hit in both level cache
            evict = 0
            if len(self.firCache) >= self.firCacheSZ:
                evict = 1
                evict_item = self.firCache.popitem(last=False)
            if evict == 1 and len(self.secCache) >= self.secCacheSZ:
                self.secCache.popitem(last=False)
            self.firCache[lba] = 1

        return hit