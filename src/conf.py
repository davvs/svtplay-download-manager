import yaml
import sys

def getConf():
    with open("conf/settings.yml", 'r') as stream:
        try:
            data = yaml.load(stream)
            dbpath=data["database"]
            series=data["series"]
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)
    return (dbpath, series)
