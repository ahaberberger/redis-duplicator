__author__ = 'andreas.haberberger'

import threading
from redisclient import RedisClient

class CopyThread(threading.Thread):

    def __init__(self, source, target, copyindicator):
        self.sourceRedis = source
        self.targetRedis = target
        self.copyindicator = copyindicator
        threading.Thread.__init__(self)

    def run(self):
        try:
            keys = self.sourceRedis.getClient().keys('%s*' % self.copyindicator)

            f = lambda s: s[len(self.copyindicator):]

            sourcekeys = frozenset(map(f, keys))
            targetkeys = frozenset(self.targetRedis.getClient().keys('*'))

            deletekeys = targetkeys.difference(sourcekeys)

            for key in deletekeys:
                self.targetRedis.getClient().delete(key)

            for key in keys:
                self.targetRedis.getClient().set(key[len(self.copyindicator):], self.sourceRedis.getClient().get(key))
        except:
            print("Error in execution!")