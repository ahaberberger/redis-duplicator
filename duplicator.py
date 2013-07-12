#!/usr/bin/env python
__author__ = 'andreas.haberberger'

import os, sys, time
from daemon import Daemon
from redisclient import RedisClient


class RedisDuplicator(Daemon):

    def initialize(self):
        self.sourceRedis = RedisClient('localhost', 6379)
        self.targetRedis = RedisClient('localhost', 6380)
        self.pubsub = self.sourceRedis.getClient().pubsub()
        self.pubsub.subscribe(['info'])

    def run(self):
        self.initialize()
        for item in self.pubsub.listen():
            #print(item['data'])
            keys = self.sourceRedis.getClient().keys('+*')
            for key in keys:
                self.targetRedis.getClient().set(key[1:], self.sourceRedis.getClient().get(key))
            #print(keys)


if __name__ == "__main__":
    daemon = RedisDuplicator('/var/tmp/duplicator.pid', stdin='/dev/stdin', stdout='/dev/stdout', stderr='/dev/stderr')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
