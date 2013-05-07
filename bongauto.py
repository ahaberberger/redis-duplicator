#!/usr/bin/env python
__author__ = 'andreas'

import os, sys, time, feedparser, json, urllib
from daemon import Daemon


class BongAuto(Daemon):

    url = ''

    def run(self):
        while True:
            fn = os.path.dirname(os.path.abspath(sys.argv[0]))
            f = open('', 'a')
            feed = feedparser.parse(self.url)
            urls = self.getUrlsFromFeed(feed)
            f.write("Ping : %s\n" % time.ctime())
            f.write("\n")
            for url in urls:
                f.write(url)
                self.downloadURL(url)
                f.write("\n")
            f.close()
            time.sleep(5)

    def getUrlsFromFeed(self, feed):
        out = []
        for item in feed['items']:
            out.append(item['link'])
        return out

    def downloadURL(self, url):
        urllib.urlretrieve(url, self.getFileName(url))

    def getFileName(self, url):
        parts = url.split('/')
        name = parts[-1]
        nameparts = name.split('_')
        outname = '_'.join(nameparts[2:])
        return '' + outname

if __name__ == "__main__":
    daemon = BongAuto('')
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
