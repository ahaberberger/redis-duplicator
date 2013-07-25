#!/usr/bin/env python
__author__ = 'andreas.haberberger'

import os, sys, yaml
from daemon import Daemon
from redisclient import RedisClient
from duplicateexceptions import RedisConnectionException, RedisCommandException
from copythread import CopyThread


class RedisDuplicator(Daemon):

    THREAD_TIMEOUT = 30

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
            sys.exit(2)
        except IOError as e:
            print(e.strerror)
            sys.exit(2)


    def run(self):
        self.initialize()
        for item in self.pubsub.listen():
            try:
                bgtask = CopyThread(self.sourceRedis, self.targetRedis, self.copyindicator)
                bgtask.start()
                bgtask.join(self.THREAD_TIMEOUT)
                if (bgtask.isAlive()):
                    try:
                        bgtask._Thread__stop()
                    except:
                        print('%s could not be terminated' % str(bgtask.getName()))
            except:
                print("Error creating worker thread!")

    def status(self):
        # Check for pidfile
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            return "running"
        else:
            return "not running"

if __name__ == "__main__":
    daemon = RedisDuplicator('/var/tmp/duplicator.pid', stdin='/dev/stdin', stdout='/dev/stdout', stderr='/dev/stderr')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'status' == sys.argv[1]:
            print(daemon.status())
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart|status" % sys.argv[0]
        sys.exit(2)
