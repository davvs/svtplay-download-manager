#!/usr/bin/env python2
import sys

from pprint import pprint

from SerieDb import SerieDb
from EpisodeDb import EpisodeDb

from conf import getConf
from database import openDb
from database import saveDb

def showSeriesStates(serieDb, db):
    print "Serie " + serieDb.name
    for id,title in serieDb.episodes.iteritems():
        ep = EpisodeDb.getFromDb(serieDb.name, id, db)
        linkOp = ep.link if ep is not None else "No link"
        print "  Ep[%s]: %s, %s" % (title[0:20], linkOp[0:20], ep.publishDate[0:22])

def main():
    (dbpath,series) = getConf()
    db = openDb(dbpath)

    for serie in series:
        name = serie["name"]
        serieDb = SerieDb.getFromDb(name, db)
        if serieDb is None:
            print "serie " + name + " is None"
        else:
            print "Showing serie " + serieDb.name
            showSeriesStates(serieDb, db)

main()
