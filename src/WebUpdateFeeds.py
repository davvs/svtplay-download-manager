#!/usr/bin/env python2
import feedparser
import textwrap
import sys
from pprint import pprint

from SerieDb import SerieDb
from EpisodeDb import EpisodeDb

from conf import getConf
from database import openDb
from database import saveDb

def updateFromFeed(serieDb, db):
    feed = feedparser.parse(serieDb.feed)
    ret = ""

    for episode in feed.entries:
        serieKey = serieDb.name + "_id_" + episode.id

        ep = EpisodeDb.getFromDb(serieDb.name, episode.id, db) or \
            EpisodeDb.create(episode.id, serieDb.name, episode.title, episode.link, episode.published)

        if not ep.id in serieDb.episodes:
            serieDb.episodes[ep.id] = ep.name
            ret += "<p>Appended %s - %s Tot episodes:%d</p>\n" % \
                (ep.id, ep.name, len(serieDb.episodes))
        ep.saveToDb(db)

    serieDb.saveToDb(db)
    return ret

def updateFeedsHtml():
    (dbpath,series) = getConf()
    db = openDb(dbpath)

    ret = ""

    for serie in series:
        name = serie["name"]
        serieDb = SerieDb.getFromDb(name, db) or \
                SerieDb.create(serie["name"], serie["feed"], serie["channel"])
        ret += "<p>Updating serie %s from feed %s</p>\n" % (name, serie["feed"])
        ret += updateFromFeed(serieDb, db)

    saveDb(db)
    return ret

def updateFeeds(requestHandler):
    requestHandler.send_response(200)
    requestHandler.send_header('Content-type', 'text/html; charset=utf-8')
    requestHandler.end_headers()
    response_text = textwrap.dedent('''\
        <html>
        <head>
            <title>Updating feeds</title>
        </head>
        <body>
            <a href="/show">Go Back</a>
            <h1>Updating feeds</h1>
            %s
        </body>
        </html>
    ''' % (updateFeedsHtml()))
    requestHandler.wfile.write(response_text.encode('utf-8'))

