#!/usr/bin/env python2
import sys
import textwrap

from pprint import pprint

from SerieDb import SerieDb
from EpisodeDb import EpisodeDb

from conf import getConf
from database import openDb
from database import saveDb

def show(requestHandler):
    requestHandler.send_response(200)
    requestHandler.send_header('Content-type', 'text/html; charset=utf-8')
    requestHandler.end_headers()
    seriesWebPart=getSeriesAsHtml()
    response_text = textwrap.dedent('''\
        <html>
        <head>
            <title>Show series</title>
        </head>
        <body>
            <form method="POST" action="/updateFeeds">
                <input type="Submit" value="Update Feeds"/>
            </form>
            <h1>All series</h1>
            %s
        </body>
        </html>
    ''' % (seriesWebPart))
    requestHandler.wfile.write(response_text.encode('utf-8'))



def showSeriesStates(serieDb, db):
    ret = ""
    for id,title in serieDb.episodes.iteritems():
        ep = EpisodeDb.getFromDb(serieDb.name, id, db)
        linkOp = ep.link if ep is not None else "No link"
        ret += "<li><b>%s</b>%s, %s</li>\n" % (title, linkOp, ep.publishDate)
    return ret

def getSeriesAsHtml():
    (dbpath,series) = getConf()
    db = openDb(dbpath)
    ret = ""

    for serie in series:
        name = serie["name"]
        serieDb = SerieDb.getFromDb(name, db)
        if serieDb is None:
            ret += "<h2>Serie " + name + " is None</h2>\n"
        else:
            ret += "<h2>Serie " + serieDb.name + "</h2>\n"
            ret += "<ul>\n%s</ul>\n" % showSeriesStates(serieDb, db)

    return ret
