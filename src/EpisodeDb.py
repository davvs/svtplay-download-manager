class EpisodeDb:
    id = None
    serieName = None
    name = None
    link = None
    downloaded = False
    interresing = False
    publishDate = None

    @classmethod
    def create(cls, id, serieName, name, link, publishDate):
        ep = EpisodeDb()
        ep.id = id
        ep.serieName = serieName
        ep.name = name
        ep.link = link
        ep.downloaded = False
        ep.interresing = False
        ep.publishDate = publishDate
        return ep
    @classmethod
    def getFromDb(cls, serieName, id, db):
        return db.get(EpisodeDb.getDbKey(serieName, id))
    @classmethod
    def getDbKey(cls, serieName, id):
        return "Episode_" + serieName + "_" + id
    @classmethod
    def getFromDb(cls, serieName, id, db):
        key = EpisodeDb.getDbKey(serieName, id)
        got = db.get(key)
        if got is None:
            return None
        return EpisodeDb.fromDict(got)
    @classmethod
    def fromDict(cls, m):
        self = EpisodeDb()
        self.id = m["id"]
        self.serieName = m["serieName"]
        self.name = m["name"]
        self.link = m["link"]
        self.downloaded = m["downloaded"]
        self.interresing = m["interresing"]
        self.publishDate = m["publishDate"]
        return self
    def toDict(self):
        a = {
                "id": self.id,
                "serieName": self.serieName,
                "name": self.name,
                "link": self.link,
                "downloaded": self.downloaded,
                "interresing": self.interresing,
                "publishDate": self.publishDate,
        }
        return a
    def saveToDb(self, db):
        return db.set(EpisodeDb.getDbKey(self.serieName, self.id), self.toDict())
