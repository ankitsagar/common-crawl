from urllib.request import urlopen, Request
import ssl
import re


def index_lister():
    # ignoring ssl certification errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = Request('http://commoncrawl.org/the-data/get-started/', headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(url).read()
    index = []
    regx = re.findall(b'(s3://.*)', html)
    for i in regx:
        reg = re.findall('\-([0-9.]*\-\d.)', i.decode())
        if len(reg) > 0 and reg[0][:4] >= '2016':
            index.append(reg)
    return index


