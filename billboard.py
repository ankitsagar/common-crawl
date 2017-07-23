import requests
import json
import gzip
from io import BytesIO
import csv
import codecs
import year_index
import html_parser

# collect all json by using index api
def json_data(index_list, domain):
    for index in index_list:
        print('for index: %s'% index[0])
        url = "http://index.commoncrawl.org/CC-MAIN-%s-index?" % index[0]
        url += "url=%s&output=json" % domain
        record_list = []
        response = requests.get(url)
        if response.status_code == 200:
            resp = response.content.splitlines()
            for res in resp:
                rsp = res.decode('UTF-8')
                record_list.append(json.loads(rsp))
            print('total item added = %d' % len(rsp))
        else:
            print('url status is not good')
        print('total data %d' % len(record_list))

    return record_list

# downloading Gzip file from common crawl
def download_data(record):
    # we don't want to download all data
    offset, length = int(record['offset']), int(record['length'])
    offset_end = offset + length - 1
    if record['status'] == '200':
        url = 'https://commoncrawl.s3.amazonaws.com/'
        # specifying the required data through header
        response = requests.get(url + record['filename'],
                                headers={'Range': 'bytes={}-{}'.format(offset, offset_end)})
        raw_data = BytesIO(response.content)
        file = gzip.GzipFile(fileobj=raw_data)
        data = file.read()
        if len(data) > 0:
            try:
                # finding and removing warc header
                warc_header = data.find(b'\r\n\r\n')
                resp = data[warc_header+4:]
                # finding and removing header
                header = resp.find(b'\r\n\r\n')
                html = resp[header+4:]
            except:
                pass
        return html
    else:
        return None
# getting all index list after 2016 from common crawl website
records_list = year_index.index_lister()
domain = 'http://www.billboard.com/charts/hot-100'

for records in records_list:
    records = [records]
    data_list = json_data(records, domain)
    for data in data_list:
        html = download_data(data)
        if html:
            # parsing data from html data of billboard website
            song, rank, artist, week = html_parser.parser(html)
            week = week[0]
            with codecs.open('week-%s.csv' % week, 'wb', encoding='utf-8') as output:
                fields = ['Rank', 'Song', 'Artist']
                logger = csv.DictWriter(output, fieldnames=fields)
                logger.writeheader()
                for i in range(len(song)):
                    logger.writerow({'Rank': rank[i], 'Song': song[i], 'Artist': artist[i]})
print('Successfully wrote all data')






