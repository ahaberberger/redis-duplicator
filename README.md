mxd-redis-sync
==============

Redis master, slave syncronization script

A demon to filter keys from one redis instance to another.
Triggered by redis pub sub.

Requirements

2 Redis instances

[Python 2.7](http://python.org/ "Python 2.7")

[PyYaml](http://stackoverflow.com/questions/14261614/how-do-i-install-the-yaml-package-for-python "PyYaml")

[redis-py](https://github.com/andymccurdy/redis-py "redis-py")


Instructions:

Copy "./config/duplicator.yml.dist" to "/etc/duplicator.yml" and adapt to local situation.
Start demon: "./duplicator.py start"
Stop demon: "./duplicator.py stop"
Restart demon: "./duplicator.py restart"

Query demon status: "./duplicator.py status"
    Exitcode 0: demon running
    Exitcode 2: demon not running

Publish on source Redis on <pubsub_channel> with any message to trigger replication

The config file:

duplicator:
    source_host: localhost # Hostname or IP of source Redis
    source_port: 6379 # Port of source Redis
    target_host: localhost # Hostname or IP of target Redis
    target_port: 6380 # Port of target Redis
    copy_indicator: + # Prefix of Keys in source Redis to be copied
    pubsub_channel: changeinfo # Name of Redis pub/sub channel on source Redis that triggers replication
