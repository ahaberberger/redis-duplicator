#!/usr/bin/env python
__author__ = 'andreas.haberberger'

import os, sys, yaml
from daemon import Daemon
from redisclient import RedisClient
from duplicateexceptions import RedisConnectionException, RedisCommandException


class RedisDuplicator(Daemon):

    def initialize(self):
        try:
            conffile = open('/etc/duplicator.yml', 'r')
            self.config = yaml.safe_load(conffile)
            conffile.close()

            self.sourceRedis = RedisClient(self.config['duplicator']['source_host'], self.config['duplicator']['source_port'])
            self.targetRedis = RedisClient(self.config['duplicator']['target_host'], self.config['duplicator']['target_port'])
            self.pubsub = self.sourceRedis.getClient().pubsub()
            self.pubsub.subscribe(self.config['duplicator']['pubsub_channel'])

            self.copyindicator = self.config['duplicator']['copy_indicator']
        except RedisConnectionException as e:
            print(e.value)
            self.stop()
        except IOError as e:
            print(e.strerror)
            self.stop()


    def run(self):
        self.initialize()
        for item in self.pubsub.listen():
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
