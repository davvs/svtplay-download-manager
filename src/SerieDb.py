import time

class SerieDb:
    name = ""
    feed = ""
    channel = ""
    lastUpdated = None
    episodes = {}

    @classmethod
    def create(cls, name, feed, channel):
        pop = SerieDb()
        pop.name = name
        pop.feed = feed
        pop.channel = channel
        pop.updated = time.time()
        pop.episodes = {}
        return pop
    @classmethod
    def getDbKey(cls, name):
        return "Serie_" + name
    @classmethod
    def getFromDb(cls, name, db):
        key = SerieDb.getDbKey(name)
        got = db.get(key)
        if got is None:
            return None
        return SerieDb.fromDict(got)
    @classmethod
    def fromDict(cls, m):
        self = SerieDb()
        self.name = m["name"]
        self.feed = m["feed"]
        self.channel = m["channel"]
        self.lastUpdated = m["lastUpdated"]
        self.episodes = m["episodes"]
        return self
    def toDict(self):
        return {
                "name": self.name,
                "feed": self.feed,
                "channel": self.channel,
                "lastUpdated": self.lastUpdated,
                "episodes": self.episodes
                }
    def saveToDb(self, db):
        return db.set(SerieDb.getDbKey(self.name), self.toDict())
