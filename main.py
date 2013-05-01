__author__ = 'andreas'

import sys
import feedparser


class BongAuto:
    url = "x"
    def __init__(self, URL):
        self.url = URL

    def run(self):
        feed = feedparser.parse(self.url)
        print(feed)


if __name__ == "__main__":
    app = BongAuto(sys.argv[1])
    app.run()
