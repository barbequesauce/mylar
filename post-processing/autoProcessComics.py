import sys
import requests
import os.path
import ConfigParser

apc_version = "2.0"

def processEpisode(dirName, nzbName=None):
    print "Your ComicRN.py script is outdated. I'll force this through, but Failed Download Handling and possible enhancements/fixes will not work and could cause errors."
    return processIssue(dirName, nzbName)

def processIssue(dirName, nzbName=None, failed=False, comicrn_version=None):

    config = ConfigParser.ConfigParser()
    configFilename = os.path.join(os.path.dirname(sys.argv[0]), "autoProcessComics.cfg")
    print "Loading config from", configFilename

    if not os.path.isfile(configFilename):
        print "ERROR: You need an autoProcessComics.cfg file - did you rename and edit the .sample?"
        sys.exit(-1)

    try:
        fp = open(configFilename, "r")
        config.readfp(fp)
        fp.close()
    except IOError, e:
        print "Could not read configuration file: ", str(e)
        sys.exit(1)

    host = config.get("Mylar", "host")
    port = config.get("Mylar", "port")
    apikey = config.get("Mylar", "apikey")
    if apikey is None:
        print("No ApiKey has been set within Mylar to allow this script to run. This is NEW. Generate an API within Mylar, and make sure to enter the apikey value into the autoProcessComics.cfg file before re-running.")
        sys.exit(1)
    try:
        ssl = int(config.get("Mylar", "ssl"))
    except (ConfigParser.NoOptionError, ValueError):
        ssl = 0

    try:
        web_root = config.get("Mylar", "web_root")
    except ConfigParser.NoOptionError:
        web_root = ""

    if ssl:
        protocol = "https://"
    else:
        protocol = "http://"

    url = protocol + host + ":" + port + web_root + '/api'

    params = {'cmd': 'forceProcess',
              'apikey': apikey,
              'nzb_folder': dirName}

    if nzbName != None:
        params['nzb_name'] = nzbName
    params['failed'] = failed

    params['apc_version'] = apc_version
    params['comicrn_version'] = comicrn_version

    try:
        print("Opening URL for post-process of %s @ %s/forceProcess:" % (dirName,url))
        pp = requests.post(url, params=params, verify=False)
    except Exception as e:
        print("Unable to open URL: %s" %e)
        sys.exit(1)

    print 'statuscode: %s' % pp.status_code

    result = pp.content

    print pp.content

    if any("Post Processing SUCCESSFUL" in s for s in result):
        return 0
    else:
        return 1
