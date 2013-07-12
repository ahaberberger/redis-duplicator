__author__ = 'andreas.haberberger'

from redisconnectionexception import RedisConnectionException
from redis import Redis
from redis.exceptions import ConnectionError

class RedisClient():
    def __init__(self, host, port):
        self.host = host
        self.port = port

        try:
            self.client = Redis(host=self.host, port=self.port)
            self.info = (self.client.info())
        except ConnectionError:
            raise RedisConnectionException("Connection to Redis on %s:%d failed!" % (self.host, self.port))

    def getPort(self):
        return self.port

    def getHost(self):
        return self.host

    def getClient(self):
        return self.client

