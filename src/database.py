import pickledb

def openDb(dbpath):
    db = pickledb.load(dbpath, True) 
    return db

def saveDb(db):
    db.dump()
