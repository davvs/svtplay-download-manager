#!/usr/bin/env python2
import feedparser
import sys
from pprint import pprint

from SerieDb import SerieDb
from EpisodeDb import EpisodeDb

from conf import getConf
from database import openDb
from database import saveDb

def updateFromFeed(serieDb, db):
    feed = feedparser.parse(serieDb.feed)

    for episode in feed.entries:
        serieKey = serieDb.name + "_id_" + episode.id

        ep = EpisodeDb.getFromDb(serieDb.name, episode.id, db) or \
            EpisodeDb.create(episode.id, serieDb.name, episode.title, episode.link, episode.published)

        if not ep.id in serieDb.episodes:
            serieDb.episodes[ep.id] = ep.name
            print "Appended " + ep.id + " - " + ep.name + " Tot %d" % len(serieDb.episodes)
        ep.saveToDb(db)

    serieDb.saveToDb(db)

def main():
    (dbpath,series) = getConf()
    db = openDb(dbpath)

    for serie in series:
        name = serie["name"]
        print "Updating " + name
        serieDb = SerieDb.getFromDb(name, db) or \
                SerieDb.create(serie["name"], serie["feed"], serie["channel"])
        updateFromFeed(serieDb, db)

    saveDb(db)

main()
